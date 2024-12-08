#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import nmap
from FunNmapLogFile import save_to_csv


def NmapScan(ip, arguments):
    # 创建 nmap.PortScanner 对象
    nm = nmap.PortScanner()

    # 执行扫描
    nm.scan(hosts=ip, arguments=arguments)

    # 获取扫描结果并格式化为 CSV
    csv_result = nm.csv()

    # 保存结果为可读的csv格式
    nm_table,logpath = save_to_csv(csv_result, nm.command_line())

    return str(nm_table),logpath

