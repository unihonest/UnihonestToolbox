# UnihonestToolbox

基于 PySide6 的现代深色科技风网络安全工具箱，采用左侧边栏导航，集成端口扫描、域名查询、DNS 分析、密码强度检测等工具。

> 🎨 深蓝黑底色 + 青蓝强调色 | 📐 适配 2560×1440 | 🧭 侧边栏导航

## 功能

| 工具 | 说明 |
|------|------|
| **Nmap 扫描** | 封装 Nmap 端口扫描，自定义参数，异步执行不阻塞 UI，结果自动保存为 CSV |
| **WHOIS 查询** | 原始 Socket 连接 WHOIS 服务器，支持自定义服务器地址 |
| **DNS 记录查询** | 支持 A / AAAA / CNAME / MX / NS / TXT / SOA / PTR / SRV / CAA / TLSA / SSHFP 共 12 种记录类型 |
| **IP 子网计算** | IPv4/IPv6 自动识别，零依赖纯本地计算 |
| **密码强度分析** | 内置 SecLists Top 200 弱口令库，支持批量检测，可一键下载完整字典 |
| **公网 IP 查询** | 多源冗余获取本机公网 IPv4/IPv6，显示国家/城市/ISP 归属信息 |

## 架构

```
UnihonestToolbox/
├── MainWindow.py              # 应用入口，侧边栏导航 + QStackedWidget
├── config/
│   ├── settings.py            # 窗口/配色/日志/工具配置
│   └── links.py               # 菜单栏 60+ 外部工具链接
├── ui/
│   ├── theme.py               # 现代深色科技风 QSS (~200行)
│   ├── widgets.py             # 控件工厂 + BasePage + 导航按钮
│   ├── tool_text.py           # 工具使用说明
│   └── pages/                 # 6 个工具面板（继承 BasePage）
├── tools/                     # 业务逻辑层（6 个工具核心）
├── font/                      # 更纱黑体等宽字体
└── utils/                     # 日志 + ASCII 艺术字
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
| PySide6 | GUI 框架 |
| python-nmap | Nmap 封装 |
| dnspython | DNS 解析 |
| prettytable | 表格格式化 |
| pyfiglet | ASCII 艺术字 |

## 许可证

GNU General Public License v3.0 — 详见 [LICENSE](LICENSE)

## 作者

[unihonest](https://github.com/unihonest)
