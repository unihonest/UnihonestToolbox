# UnihonestToolbox

基于 PyQt6 的网络安全工具箱，集成 Nmap 扫描、Whois 查询、DNS 记录分析等常用安全工具，提供统一的操作界面与日志管理。

## 功能

| 工具 | 说明 |
|------|------|
| **Nmap 扫描** | 封装 Nmap 端口扫描，支持自定义参数，结果自动保存为 CSV |
| **WHOIS 查询** | 原始 Socket WHOIS 查询，支持自定义 WHOIS 服务器 |
| **DNS 查询** | 支持 A / AAAA / CNAME / MX / NS / TXT / SOA / PTR / SRV / CAA / TLSA / SSHFP 共 12 种记录类型 |
| **命令执行** | 内建终端，支持任意 Shell 命令 |

## 架构

```
UnihonestToolbox/
├── MainWindow.py          # 入口，工具路由
├── config/                # 应用配置与菜单链接
├── ui/                    # 界面层（主题、控件工厂、工具面板）
├── tools/                 # 业务逻辑层（Nmap / DNS / Whois）
└── utils/                 # 辅助模块（字体加载、日志）
```

## 环境要求

- Python ≥ 3.12
- 系统已安装 [Nmap](https://nmap.org/download)（Nmap 功能需要）

## 快速开始

```bash
git clone https://github.com/unihonest/UnihonestToolbox.git
cd UnihonestToolbox

# 推荐使用 Conda 虚拟环境
conda create -n UnihonestToolbox python=3.12.7 -y
conda activate UnihonestToolbox

# 安装依赖
pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple

# 运行
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
