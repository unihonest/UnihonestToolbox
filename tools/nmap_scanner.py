# -*- coding: utf-8 -*-
"""Nmap 扫描 + CSV 日志"""

import csv
from datetime import datetime
from pathlib import Path

import nmap
from prettytable import PrettyTable, ALL

from config.settings import LOG_DIRS


def _validate_ip(ip: str) -> bool:
    """简单的 IP/域名校验"""
    if not ip or not ip.strip():
        return False
    return True


def _save_to_csv(data: str, nmcommand: str) -> tuple:
    """保存扫描结果为 CSV 并生成 PrettyTable"""
    log_folder = LOG_DIRS["nmap"]
    script_dir = Path(__file__).parent.parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"nmap_{current_time}.csv"
    logpath = log_path / log_file_name

    rows = []
    reader = csv.reader(data.splitlines(), delimiter=";", quotechar='"')
    for row in reader:
        rows.append(row)

    with open(logpath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=",")
        writer.writerows(rows)

    nmtable = _csv_to_table(logpath)

    with open(logpath, mode="a", encoding="utf-8") as f:
        f.write(f'NmapCommand,"{nmcommand}"\n')

    return str(nmtable), str(logpath)


def _csv_to_table(logpath: Path) -> PrettyTable:
    """CSV 转 PrettyTable"""
    table = PrettyTable()
    table.hrules = ALL
    table.align = "l"

    with open(logpath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        table.field_names = headers
        table.max_width = 20
        for row in reader:
            if len(row) == len(headers):
                table.add_row(row)
    return table


def NmapScan(ip: str, arguments: str = "") -> tuple:
    """执行 Nmap 扫描，返回 (表格字符串, 日志路径)"""
    if not _validate_ip(ip):
        return "Error: 请输入有效的目标 IP 或域名", ""

    nm = nmap.PortScanner()
    nm.scan(hosts=ip, arguments=arguments)
    csv_result = nm.csv()
    return _save_to_csv(csv_result, nm.command_line())
