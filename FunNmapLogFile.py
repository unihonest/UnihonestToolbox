#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import csv
from prettytable import PrettyTable, ALL
from datetime import datetime
from pathlib import Path


def save_to_csv(data, nmcommand):
    # 获取当前脚本文件的路径
    log_folder='nmaplog'
    script_dir = Path(__file__).parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"nmap_{current_time}.csv"
    logpath = log_path / log_file_name
    
    # 读取并解析原始数据，使用分号作为分隔符
    rows = []
    reader = csv.reader(data.splitlines(), delimiter=';', quotechar='"')
    for row in reader:
        rows.append(row)

    # 写入 CSV 文件，并为所有字段加上双引号，使用逗号作为分隔符
    with open(logpath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=',')  # 使用逗号作为分隔符
        writer.writerows(rows)

    nmtable = csv_to_table(logpath)

    # 写入Nmap信息
    with open(logpath, mode='a', encoding='utf-8') as file:
        new_content = []
        new_content.append(f"NmapCommand,\"{nmcommand}\"")
        for line in new_content:
            file.write(line + "\n")
    
    return nmtable,str(logpath)

    
def csv_to_table(logpath):
    table = PrettyTable()

    # 设置表格样式和对齐方式
    table.hrules = ALL  # 为所有行添加水平线
    table.align = "l"   # 左对齐文本

    # 打开并读取 CSV 文件
    with open(logpath, 'r') as file:
        reader = csv.reader(file)
        
        # 读取表头
        headers = next(reader)
        table.field_names = headers
        
        # 为每一列设置最大宽度，并允许自动换行
        for field in headers:
            table.max_width[field] = 20  # 设置每个字段的最大宽度
            table._valign[field] = "t"   # 文本顶部对齐

        # 读取每一行并添加到表格
        for row in reader:
            table.add_row(row)

    # 输出表格
    return table