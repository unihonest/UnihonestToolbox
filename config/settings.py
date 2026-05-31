# -*- coding: utf-8 -*-
"""应用配置"""

# 窗口设置
WINDOW_WIDTH = 739
WINDOW_HEIGHT = 500
WINDOW_TITLE = "网络安全工具箱 - unihonest"

# 日志目录（相对于项目根目录，统一放在 UserLog 下）
USER_LOG_DIR = "UserLog"
LOG_DIRS = {
    "nmap": f"{USER_LOG_DIR}/nmap",
    "dns": f"{USER_LOG_DIR}/dns",
    "whois": f"{USER_LOG_DIR}/whois",
    "app": f"{USER_LOG_DIR}/app",
}

# 工具默认参数
DEFAULT_DNS_SERVER = "8.8.8.8"
DEFAULT_WHOIS_SERVER = "whois.iana.org"
DEFAULT_NMAP_ARGS = "-Pn -sS -sV -O -T3 -p22,80,443,3389"

# 可用工具列表（显示名, 模块路径）
TOOLS = [
    ("Nmap", "ui.pages.nmap_page"),
    ("Whois", "ui.pages.whois_page"),
    ("DNS-type", "ui.pages.dns_page"),
]
