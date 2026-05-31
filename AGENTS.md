# Project Guidelines

## Build and Run

```bash
# 推荐使用 conda 虚拟环境
conda create -n unihonest python=3.12.7
conda activate unihonest
pip install -r requirements.txt -i https://mirrors.ustc.edu.cn/pypi/simple
python MainWindow.py
```

**注意**：Nmap 功能要求系统已安装 `nmap` 可执行文件。

## Architecture

单文件 GUI 应用，`MainWindow.py` 是入口与核心控制器。六个功能模块被作为函数导入：

| 模块 | 导出函数 | 用途 |
|------|---------|------|
| `FunNmapScanner.py` | `NmapScan(ip, arguments)` | Nmap 扫描 → 调用 `FunNmapLogFile` 保存 CSV |
| `FunNmapLogFile.py` | `save_to_csv()`, `csv_to_table()` | CSV 日志 + PrettyTable 格式化 |
| `FunDNSType.py` | `save_dns_records_to_log(domain, dns_servers)` | DNS 多类型记录查询 |
| `FunWhoisInfo.py` | `whois_txt(domain)` | 原始 socket WHOIS 查询 |
| `FunReverseShell.py` | `update_shell_reverse(ip, port, format)`, `shell_to_base64(text, option)` | 反弹 Shell 命令生成 |
| `GetDarkCSS.py` | `darkcss()` | Qt 暗色主题样式表 |
| `GetMenubarLink.py` | `get_manu_link()` | 返回 3 个字典：渗透测试、应急响应、新闻资讯 |
| `GetToolTXT.py` | `get_tool_txt(value)` | 工具使用说明文档 |

`MainWindow` 是唯一的类（`QMainWindow` 子类），所有 UI 通过 `__init__` 内的嵌套工厂函数 `add_label/input/textarea/button` 构建，布局为 `QVBoxLayout` + `QGridLayout` → `QFrame` → `QScrollArea`。

## Code Style

- 所有文件 UTF-8 + `# -*- coding: utf-8 -*-`，中文注释和字符串普遍存在
- 公开函数：`snake_case`（如 `save_dns_records_to_log`, `get_manu_link`）
- 类名：`PascalCase`（仅 `MainWindow`）
- 槽函数：`on_` 前缀（如 `on_button_click`, `on_combobox_ToolTXT`）
- 模块文件：`Get`/`Fun` 前缀 + PascalCase（如 `FunNmapScanner.py`, `GetDarkCSS.py`）
- 实例变量：`snake_case`（如 `self.result_area`, `self.unihonest_input1`）

## PyQt6 Patterns

- **控件工厂**：`MainWindow.__init__` 内定义的嵌套函数创建控件并添加到网格布局，不可移到类外部。
- **Placeholder 实现**：通过直接替换 `QLineEdit.focusInEvent` / `focusOutEvent` 实现（monkey-patch，非子类化重写）。创建新 `QLineEdit` 时需复制此模式。
- **样式**：全局 `app.setStyleSheet(darkcss())`，个别控件可用 `widget.setStyleSheet()` 覆盖。
- **线程**：子进程通过 `threading.Thread(daemon=True)` + `QTimer(50ms)` + `threading.Lock()` 异步运行。
- **菜单**：`get_manu_link()` 返回 3 个嵌套字典的元组，用索引 `[0]`/`[1]`/`[2]` 访问。

## Gotchas

1. **Lambda 闭包陷阱**：菜单链接回调用 `lambda checked, u=url: webbrowser.open(u)`（默认参数捕获），不要简化为 `lambda: webbrowser.open(url)`。
2. **`MainWindow.py` 第 239 行**：`save_dns_records_to_log(input1, )` 缺少第二个参数 `dns_servers`，调用会失败。
3. **无外部配置文件**：所有配置硬编码在源码中（日志路径、窗口大小 739×500、URL 列表）。
4. **日志目录**：运行时在脚本所在目录创建 `nmaplog/`、`dnstypelog/`、`whoislog/`。
5. **字体**：优先加载本地 `SarasaFixedSC-Light.ttf`，失败时回退 `Consolas`。
