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
    elif value == "弱口令检测":
        return _normalize(
            "密码强度分析工具\n\n"
            "内置 Top 200 常见弱口令库（来源 SecLists/RockYou），\n"
            "从 5 个维度检测密码强度：\n"
            "弱口令库命中 / 长度 / 字符类型 / 重复模式 / 键盘序列\n\n"
            '点击"下载完整字典"可获取 Top 10000 弱口令库。\n\n'
            "举🌰:\n"
            "输入: admin123"
        )
    return ""
