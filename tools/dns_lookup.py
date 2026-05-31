# -*- coding: utf-8 -*-
"""DNS 多类型记录查询"""

from datetime import datetime
from pathlib import Path

import dns.resolver

from config.settings import LOG_DIRS, DEFAULT_DNS_SERVER
from utils.logger import logger

RECORD_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "PTR", "SRV", "CAA", "TLSA", "SSHFP"]


def _get_dns_record(domain: str, record_type: str, resolver: dns.resolver.Resolver) -> list:
    """查询单种 DNS 记录"""
    try:
        answers = resolver.resolve(domain, record_type)
        if record_type == "MX":
            return [(rdata.exchange.to_text(), rdata.preference) for rdata in answers]
        else:
            return [rdata.to_text() for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []
    except Exception as e:
        logger.error(f"Error getting {record_type} records for {domain}: {e}")
        return []


def _get_all_records(domain: str, dns_server: str) -> dict:
    """查询所有 DNS 记录类型"""
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [dns_server]

    for record_type in RECORD_TYPES:
        records[record_type] = _get_dns_record(domain, record_type, resolver)

    return records


def save_dns_records_to_log(domain: str, dns_servers: str = DEFAULT_DNS_SERVER) -> tuple:
    """查询 DNS 记录并保存日志，返回 (内容, 日志路径)"""
    if not domain or not domain.strip():
        return "Error: 请输入有效的域名", ""

    dns_records = _get_all_records(domain.strip(), dns_servers or DEFAULT_DNS_SERVER)

    log_folder = LOG_DIRS["dns"]
    script_dir = Path(__file__).parent.parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"dnstype_{current_time}.log"
    log_file_path = log_path / log_file_name

    with open(log_file_path, mode="w", encoding="utf-8") as f:
        f.write(f'DNS Records for "{domain}":\n\n')
        for record_type, record_list in dns_records.items():
            if record_list:
                f.write(f"{record_type.upper()} Records:\n")
                for record in record_list:
                    f.write(f"  {record}\n")
                f.write("\n")

    with open(log_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    return content, str(log_file_path)
