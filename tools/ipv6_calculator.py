# -*- coding: utf-8 -*-
"""IPv6 子网计算器"""

import ipaddress


def calculate_ipv6(text: str) -> str:
    """解析 IPv6/CIDR 并返回详细子网信息"""
    text = text.strip()
    if not text:
        return "请输入 IPv6/CIDR 格式，如 2001:db8::1/64"

    try:
        net = ipaddress.IPv6Network(text, strict=False)
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        return "格式错误。请使用: 2001:db8::1/64 或 fe80::1/10"

    # 仅小子网计算地址范围（前缀 ≥ 120，即 ≤ 256 个地址）
    show_range = net.prefixlen >= 120 and net.num_addresses <= 256
    if show_range:
        hosts = list(net.hosts())
        usable = hosts[0] if hosts else None
        last_usable = hosts[-1] if hosts else None

    # IP 类型
    if net.is_private:
        ip_type = "唯一本地地址 (ULA)"
    elif net.is_loopback:
        ip_type = "环回地址"
    elif net.is_link_local:
        ip_type = "链路本地地址"
    elif net.is_multicast:
        ip_type = "组播地址"
    elif net.is_global:
        ip_type = "全球单播地址"
    else:
        ip_type = "其他"

    # 地址缩写和完整形式
    compressed = str(net.network_address)
    exploded = net.network_address.exploded

    lines = []
    lines.append("═" * 60)
    lines.append(" IPv6 子网计算报告")
    lines.append("═" * 60)
    lines.append(f" 输入地址:{text}")
    lines.append(f" 网络地址:{compressed}")
    lines.append(f" 完整格式:{exploded}")
    lines.append(f" 前缀长度:/{net.prefixlen}")
    if show_range:
        lines.append(f" 地址范围:{usable} - {last_usable}")
    lines.append(f" 总地址数:{net.num_addresses:,}")
    lines.append(f" 地址类型:{ip_type}")
    lines.append("═" * 60)

    return "\n".join(lines)
