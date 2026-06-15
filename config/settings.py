# -*- coding: utf-8 -*-
"""应用配置"""

# 窗口设置 (适配 2560×1440 屏幕)
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900
WINDOW_TITLE = "Unihonest Toolbox"

# 现代深色科技风配色
COLORS = {
    "bg_primary": "#1a1a2e",
    "bg_secondary": "#16213e",
    "bg_card": "#1f2b47",
    "bg_hover": "#253553",
    "accent": "#4fc3f7",
    "accent_hover": "#7fd8fa",
    "text_primary": "#e0e0e0",
    "text_secondary": "#8899aa",
    "border": "#2a3a5c",
    "success": "#66bb6a",
    "warning": "#ffa726",
    "danger": "#ef5350",
    "sidebar_width": 200,
}

# 日志目录（相对于项目根目录，统一放在 UserLog 下）
USER_LOG_DIR = "UserLog"
LOG_DIRS = {
    "nmap": f"{USER_LOG_DIR}/nmap",
    "dns": f"{USER_LOG_DIR}/dns",
    "whois": f"{USER_LOG_DIR}/whois",
    "app": f"{USER_LOG_DIR}/app",
}

# 网络代理（Clash / 系统代理）
HTTP_PROXY = "127.0.0.1:7897"

# 工具默认参数
DEFAULT_DNS_SERVER = "8.8.8.8"
DEFAULT_WHOIS_SERVER = "whois.iana.org"

# 侧边栏工具导航（图标, 名称）
NAV_ITEMS = [
    ("📡", "Nmap"),
    ("🌐", "Whois"),
    ("🔍", "DNS-type"),
    ("🔢", "IP计算器"),
    ("🔑", "弱口令检测"),
    ("🌍", "公网IP查询"),
]
