#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

# 工具的使用文档
def get_tool_txt(value):
    if value == "OneForAll":
        tool_txt = f"子域收集工具: https://github.com/shmilylty/OneForAll\n查看帮助: python oneforall.py -h\n禁用字典测试: python oneforall.py --target domain.com --brute False run\n"
        return tool_txt
    
    elif value == "Nmap":
        tool_txt = f"nmap 功能需在本地安装 nmap 软件。\n下载: https://nmap.org/download\n校验 hash: https://nmap.org/dist/sigs/\n\n举🌰: \n输入框1: localhost\n输入框2: -Pn -sS -sV -O -T3 -p22,80,443,3389"
        return tool_txt
    
    elif value == "Whois":
        tool_txt = f"使用whois查询时, 需根据是否返回\"refer\"字段，更换 whois 服务器。\n\n举🌰: \n输入框1: unihonest.github.io\n输入框2: whois.iana.org"
        return tool_txt

    elif value == "DNS-type":
        tool_txt = f"使用DNS查询DNS的各种记录类型。以下为查询列表: \n['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'PTR', 'SRV', 'CAA', 'TLSA', 'SSHFP']\n\n举🌰: \n输入框1: unihonest.github.io\n输入框2: 8.8.8.8"
        return tool_txt