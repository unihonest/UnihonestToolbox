# UnihonestToolbox

基于 PyQt6 的网络安全工具箱，集成端口扫描、域名查询、DNS 分析、密码强度检测等工具，提供统一的图形界面与日志管理。

## 功能

| 工具 | 说明 |
|------|------|
| **Nmap 扫描** | 封装 Nmap 端口扫描，自定义参数，结果自动保存为 CSV 并格式化展示 |
| **WHOIS 查询** | 原始 Socket 连接 WHOIS 服务器，支持自定义服务器地址 |
| **DNS 记录查询** | 支持 A / AAAA / CNAME / MX / NS / TXT / SOA / PTR / SRV / CAA / TLSA / SSHFP 共 12 种记录类型 |
| **密码强度分析** | 内置 SecLists Top 200 弱口令库，支持批量检测，可一键下载完整字典 |
| **命令执行** | 内建 Shell 终端，异步执行不阻塞 UI，支持中断 |

## 架构

```
UnihonestToolbox/
├── MainWindow.py              # 应用入口，工具路由与菜单管理
├── config/
│   ├── settings.py            # 窗口、日志、默认参数
│   └── links.py               # 菜单栏 60+ 外部工具链接
├── ui/
│   ├── theme.py               # 暗色主题 QSS
│   ├── widgets.py             # 可复用控件工厂
│   ├── tool_text.py           # 工具使用说明
│   └── pages/                 # 工具面板（Nmap / DNS / Whois / 密码 / 命令）
├── tools/
│   ├── nmap_scanner.py        # Nmap 扫描 + CSV 日志
│   ├── dns_lookup.py          # DNS 多类型记录查询
│   ├── whois_query.py         # 原始 Socket WHOIS
│   └── password_checker.py   # 密码强度分析 + 字典下载
└── utils/
    ├── helpers.py              # 字体加载、ASCII 艺术字
    └── logger.py               # 统一日志系统
```

## 环境要求

- Python ≥ 3.12
- 系统需安装 [Nmap](https://nmap.org/download)（仅 Nmap 功能需要，其余工具无需）

## 快速开始

```bash
git clone https://github.com/unihonest/UnihonestToolbox.git
cd UnihonestToolbox

conda create -n UnihonestToolbox python=3.12.7 -y
conda activate UnihonestToolbox

pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple

python MainWindow.py
```

## 依赖

| 包 | 用途 |
|------|------|
| PyQt6 | GUI 框架 |
| python-nmap | Nmap 封装 |
| dnspython | DNS 解析 |
| prettytable | 表格格式化 |
| pyfiglet | ASCII 艺术字 |

## 许可证

GNU General Public License v3.0 — 详见 [LICENSE](LICENSE)

## 作者

[unihonest](https://github.com/unihonest)
