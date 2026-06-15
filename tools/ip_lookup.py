# -*- coding: utf-8 -*-
"""公网 IP 查询工具"""

import json
import ssl
import urllib.request

from utils.settings_manager import get_proxy, is_proxy_enabled

# 多个查询源，按优先级排列（ip-api 优先，含归属地信息）
SOURCES = [
    {
        "name": "ip-api.com",
        "url4": "http://ip-api.com/json/?fields=61439",
        "url6": None,
        "geo": True,
    },
    {
        "name": "ipify",
        "url4": "https://api.ipify.org?format=json",
        "url6": "https://api6.ipify.org?format=json",
        "geo": False,
    },
    {
        "name": "ifconfig.me",
        "url4": "https://ifconfig.me/all.json",
        "url6": None,
        "geo": False,
    },
]


def _build_opener():
    """根据代理设置构建 opener"""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    https_handler = urllib.request.HTTPSHandler(context=context)

    if is_proxy_enabled():
        proxy_addr = get_proxy()
        proxy = urllib.request.ProxyHandler({
            "http": f"http://{proxy_addr}",
            "https": f"http://{proxy_addr}",
        })
        opener = urllib.request.build_opener(proxy, https_handler)
    else:
        opener = urllib.request.build_opener(https_handler)
    return opener


def _fetch_json(url: str, timeout: int = 10) -> dict:
    """通用 JSON 请求"""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) UnihonestToolbox/2.0",
    })
    with _build_opener().open(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_public_ip() -> str:
    """获取本机公网 IPv4 和 IPv6 地址，返回格式化报告"""
    lines = []
    lines.append("═" * 44)
    lines.append(" 公网 IP 查询")
    lines.append("═" * 44)

    # ── IPv4 ──
    v4 = None
    for src in SOURCES:
        try:
            data = _fetch_json(src["url4"])
            if src["name"] == "ipify":
                v4 = data.get("ip", "")
            elif src["name"] == "ifconfig.me":
                v4 = data.get("ip_addr", "")
            elif src["name"] == "ip-api.com":
                v4 = data.get("query", "")
            if v4:
                lines.append(f" IPv4:  {v4}")
                lines.append(f" 来源:  {src['name']}")
                # ip-api 有额外信息
                if src["name"] == "ip-api.com":
                    lines.append(f" 归属:  {data.get('country','')} {data.get('regionName','')} "
                                 f"{data.get('city','')}")
                    isp = data.get("isp", "")
                    if isp:
                        lines.append(f" ISP:   {isp}")
                break
        except Exception:
            continue

    if not v4:
        lines.append(" IPv4:  查询失败（请检查网络或代理设置）")

    # ── IPv6 ──
    v6 = None
    for src in SOURCES:
        if not src["url6"]:
            continue
        try:
            data = _fetch_json(src["url6"])
            if src["name"] == "ipify":
                v6 = data.get("ip", "")
            if v6:
                lines.append(f" IPv6:  {v6}")
                break
        except Exception:
            continue

    if not v6:
        lines.append(" IPv6:  未检测到（可能当前网络不支持 IPv6）")

    lines.append("═" * 44)

    return "\n".join(lines)
