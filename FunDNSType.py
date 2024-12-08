#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import dns.resolver
import logging
from datetime import datetime
from pathlib import Path


# 设置日志配置
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_dns_record(domain, record_type, resolver):
    try:
        answers = resolver.resolve(domain, record_type)
        if record_type == 'MX':
            return [(rdata.exchange.to_text(), rdata.preference) for rdata in answers]
        else:
            return [rdata.to_text() for rdata in answers]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return []
    except Exception as e:
        logging.error(f"Error getting {record_type} records for {domain}: {e}")
        return []


def get_all_dns_records(domain, dns_servers):
    records = {}
    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = [dns_servers]

    # 定义要查询的记录类型及其处理方式
    record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'PTR', 'SRV', 'CAA', 'TLSA', 'SSHFP']

    for record_type in record_types:
        records[record_type] = get_dns_record(domain, record_type, my_resolver)

    return records


def save_dns_records_to_log(domain, dns_servers):
    dns_records = get_all_dns_records(domain, dns_servers)
    log_folder='dnstypelog'
    script_dir = Path(__file__).parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"dnstype_{current_time}.log"
    log_file_path = log_path / log_file_name

    with open(log_file_path, mode='w', encoding='utf-8') as file:
        file.write(f"DNS Records for \"{domain}\" :\n\n")
        for record_type, record_list in dns_records.items():
            if record_list:
                file.write(f"{record_type.upper()} Records:\n")
                for record in record_list:
                    file.write(f"  {record}\n")
                file.write("\n")

    with open(log_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        file.close()

    return content,str(log_file_path)

