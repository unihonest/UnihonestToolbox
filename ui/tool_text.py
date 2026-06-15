# -*- coding: utf-8 -*-
"""工具使用说明文档"""

import re


def _normalize(text: str) -> str:
    return re.sub(r"[^\S\n]+", " ", text)


def get_tool_txt(value: str) -> str:
    if value == "Nmap":
        return _normalize(
            "Nmap 端口扫描 — 封装 Nmap 引擎，扫描目标主机开放端口、"
            "服务版本与操作系统指纹，结果自动保存为 CSV 日志。\n"
            "⚠ 使用前需在本地安装 Nmap: https://nmap.org/download\n\n"
            "举🌰:\n"
            "目标主机: 192.168.1.1\n"
            "参数: -Pn -sS -sV -O -T3 -p22,80,443,3389\n\n"
            '常用参数:\n'
            "  -sS  TCP SYN 扫描\n"
            "  -sV  服务版本探测\n"
            "  -O   操作系统识别\n"
            "  -T3  时间模板(0-5)\n"
            "  -p-  扫描全部 65535 端口"
        )
    elif value == "Whois":
        return _normalize(
            "WHOIS 域名查询 — 通过原始 Socket 连接 WHOIS 服务器，"
            "查询域名注册人、注册商、创建/过期时间等信息。\n"
            "支持自定义 WHOIS 服务器地址，自动处理 Refer 跳转。\n\n"
            "举🌰:\n"
            "域名: unihonest.github.io\n"
            "WHOIS 服务器: whois.iana.org\n\n"
            "常用 WHOIS 服务器:\n"
            "  whois.iana.org      IANA 根服务器\n"
            "  whois.verisign-grs.com   .com/.net\n"
            "  whois.pir.org        .org\n"
            "  whois.cnnic.cn       .cn"
        )
    elif value == "DNS-type":
        return _normalize(
            "DNS 记录查询 — 使用 dnspython 查询域名的 12 种 DNS 记录类型，"
            "支持自定义 DNS 服务器。\n"
            "支持类型: A / AAAA / CNAME / MX / NS / TXT / SOA / "
            "PTR / SRV / CAA / TLSA / SSHFP\n\n"
            "举🌰:\n"
            "域名: unihonest.github.io\n"
            "DNS 服务器: 8.8.8.8"
        )
    elif value == "弱口令检测":
        return _normalize(
            "弱口令检测 — 基于 SecLists Top 200 弱口令库，从 5 个维度分析密码强度: "
            "弱口令库命中 / 长度 / 字符类型 / 重复模式 / 键盘序列。\n"
            "支持单个检测与批量检测，可一键下载 Top 10000 完整字典。\n\n"
            "举🌰:\n"
            "输入: admin123\n\n"
            "强度等级:\n"
            "  🔴 弱   — 命中弱口令库或长度过短\n"
            "  🟠 一般 — 字符类型单一\n"
            "  🟡 中等 — 长度/类型达标但有模式缺陷\n"
            "  🟢 强   — 长度≥12 且含大小写+数字+特殊字符"
        )
    elif value == "IP计算器":
        return _normalize(
            "IP 子网计算器 — 自动识别 IPv4/IPv6 地址，输入 IP/CIDR 格式"
            "即可计算完整子网信息，纯本地运算零依赖。\n"
            "IPv4: 网络地址 / 广播地址 / 子网掩码 / 反掩码 / 地址范围 / "
            "可用地址数 / 类型(公网/私网/回环) / 二进制\n"
            "IPv6: 网络地址 / 完整格式 / 前缀长度 / 地址范围 / 总地址数 / "
            "地址类型(全球单播/链路本地/回环/ULA)\n\n"
            "举🌰:\n"
            "  192.168.1.1/24\n"
            "  10.0.0.0/8\n"
            "  2001:db8::1/64\n"
            "  fe80::1/10"
        )
    elif value == "公网IP查询":
        return _normalize(
            "公网 IP 查询 — 自动获取本机公网 IPv4/IPv6 地址，"
            "多源冗余查询（ipify / ifconfig.me / ip-api），显示归属地和运营商。\n"
            "查询优先级: IPv4 依次尝试多源 → IPv6 通过 ipify6 获取\n\n"
            "点击「查询本机公网 IP」按钮即可，无需额外输入。\n\n"
            "注意:\n"
            "  国内网络建议开启代理（设置 → 代理设置）\n"
            "  IPv6 需当前网络环境支持"
        )
    return ""
