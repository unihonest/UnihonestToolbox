# -*- coding: utf-8 -*-
"""工具使用说明文档"""

import re


def _normalize(text: str) -> str:
    return re.sub(r"[^\S\n]+", " ", text)


def get_tool_txt(value: str) -> str:
    if value == "Nmap":
        return _normalize(
            "nmap 功能需在本地安装 nmap 软件。\n"
            "下载: https://nmap.org/download\n"
            "校验 hash: https://nmap.org/dist/sigs/\n\n"
            "举🌰:\n"
            "输入框1: localhost\n"
            "输入框2: -Pn -sS -sV -O -T3 -p22,80,443,3389"
        )
    elif value == "Whois":
        return _normalize(
            '使用whois查询时, 需根据是否返回"refer"字段，更换 whois 服务器。\n\n'
            "举🌰:\n"
            "输入框1: unihonest.github.io\n"
            "输入框2: whois.iana.org"
        )
    elif value == "DNS-type":
        return _normalize(
            "使用dnspython查询DNS的各种记录类型。以下为查询列表:\n"
            "['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'PTR', 'SRV', 'CAA', 'TLSA', 'SSHFP']\n\n"
            "举🌰:\n"
            "输入框1: unihonest.github.io\n"
            "输入框2: 8.8.8.8\n\n"
            "也可以在Command执行如下命令：\n"
            "nslookup unihonest.github.io\n"
            "nslookup -type=A unihonest.github.io\n"
            "nslookup -query=any unihonest.github.io\n"
            "nslookup unihonest.github.io 8.8.8.8"
        )
    return ""
