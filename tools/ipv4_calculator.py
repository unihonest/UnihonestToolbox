# -*- coding: utf-8 -*-
"""IPv4 子网计算器"""

import ipaddress


def calculate_ipv4(text: str) -> str:
    """解析 IP/CIDR 并返回详细子网信息"""
    text = text.strip()
    if not text:
        return "请输入 IP/CIDR 格式，如 192.168.1.100/24"

    # 尝试直接解析 IP/CIDR
    try:
        net = ipaddress.IPv4Network(text, strict=False)
    except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError):
        pass
    else:
        return _format_report(net, text)

    # 尝试 IP + 掩码分开的形式
    parts = text.split()
    if len(parts) == 2:
        for sep in ["/", " "]:
            combined = f"{parts[0]}/{parts[1]}"
            try:
                net = ipaddress.IPv4Network(combined, strict=False)
                return _format_report(net, text)
            except (ValueError, ipaddress.AddressValueError, ipaddress.NetmaskValueError):
                continue

    return "格式错误。请使用: 192.168.1.100/24 或 192.168.1.100 255.255.255.0"


def _format_report(net: ipaddress.IPv4Network, raw_input: str = "") -> str:
    """生成格式化的子网报告"""
    # 仅小子网枚举地址范围（≤65536 个地址），大子网跳过避免卡死
    total_hosts = net.num_addresses - 2 if net.num_addresses > 2 else 0
    show_range = net.num_addresses <= 65536
    if show_range:
        hosts = list(net.hosts())
        usable = hosts[0] if hosts else None
        last_usable = hosts[-1] if hosts else None

    # IP 类型
    if net.is_private:
        ip_type = "私有地址"
    elif net.is_loopback:
        ip_type = "环回地址"
    elif net.is_link_local:
        ip_type = "链路本地"
    else:
        ip_type = "公网地址"

    # 地址类
    first = int(str(net.network_address).split(".")[0])
    if first < 128:
        ip_class = "A 类"
    elif first < 192:
        ip_class = "B 类"
    elif first < 224:
        ip_class = "C 类"
    elif first < 240:
        ip_class = "D 类（组播）"
    else:
        ip_class = "E 类（保留）"

    # 二进制
    def _to_bin(addr):
        return ".".join(f"{int(o):08b}" for o in str(addr).split("."))

    lines = []
    lines.append("═" * 44)
    lines.append(" IPv4 子网计算报告")
    lines.append("═" * 44)
    lines.append(f" 输入地址:{raw_input}")
    lines.append(f" 网络地址:{net.network_address}")
    lines.append(f" 广播地址:{net.broadcast_address}")
    lines.append(f" 子网掩码:{net.netmask}")
    lines.append(f" 反掩码 :{net.hostmask}")
    if show_range and usable and last_usable:
        lines.append(f" 地址范围:{usable} - {last_usable}")
    elif not show_range:
        lines.append(f" 地址范围:<子网过大({net.num_addresses}个地址)，已跳过>")
    lines.append(f" 可用地址:{total_hosts}")
    lines.append(f" 总地址数:{net.num_addresses}")
    lines.append(f" 地址类型:{ip_type} ({ip_class})")
    lines.append("─" * 44)
    lines.append(f" 二进制地址{_to_bin(net.network_address)}")
    lines.append(f" 二进制掩码{_to_bin(net.netmask)}")
    lines.append("═" * 44)

    return "\n".join(lines)
