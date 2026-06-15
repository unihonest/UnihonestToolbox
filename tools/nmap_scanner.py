# -*- coding: utf-8 -*-
"""Nmap 扫描 + CSV 日志"""

import csv
import os
from datetime import datetime
from pathlib import Path

import nmap
from prettytable import PrettyTable, ALL

from config.settings import LOG_DIRS

# Windows 常见 Nmap 安装路径（python-nmap 默认只搜 PATH）
_NMAP_SEARCH = [
    r"C:\Program Files (x86)\Nmap\nmap.exe",
    r"C:\Program Files\Nmap\nmap.exe",
]
if os.name == "nt":
    _NMAP_SEARCH.append("nmap.exe")
else:
    _NMAP_SEARCH.append("nmap")


def _validate_ip(ip: str) -> bool:
    """IP/域名校验：拒绝空输入和 Shell 特殊字符"""
    if not ip or not ip.strip():
        return False
    # 防止命令注入，拒绝 Shell 元字符
    dangerous = {";", "&", "|", "`", "$", "(", ")", "{", "}", "<", ">", "\n", "\r"}
    if any(c in ip for c in dangerous):
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

    nm = nmap.PortScanner(nmap_search_path=_NMAP_SEARCH)
    nm.scan(hosts=ip, arguments=arguments)
    csv_result = nm.csv()
    return _save_to_csv(csv_result, nm.command_line())
