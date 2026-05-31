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

单文件 GUI 应用 → 已重构为分层架构，`MainWindow.py` 是轻量入口和路由控制器。

```
UnihonestToolbox/
├── MainWindow.py              # 入口，QTabWidget + 工具路由
├── config/
│   ├── settings.py            # 窗口大小、日志路径、默认参数
│   └── links.py               # 菜单栏外部链接数据
├── ui/
│   ├── theme.py               # 暗色主题 QSS 样式 (原 GetDarkCSS)
│   ├── widgets.py             # 可复用控件工厂
│   ├── tool_text.py           # 工具使用说明 (原 GetToolTXT)
│   └── pages/
│       ├── nmap_page.py       # Nmap 扫描面板
│       ├── dns_page.py        # DNS 查询面板
│       ├── whois_page.py      # WHOIS 查询面板
│       ├── shell_page.py      # 反弹Shell/Base64 面板
│       └── cmd_page.py        # 命令执行面板
├── tools/
│   ├── nmap_scanner.py        # Nmap 扫描 + CSV 日志
│   ├── dns_lookup.py          # DNS 多类型记录查询
│   ├── whois_query.py         # 原始 socket WHOIS
│   └── reverse_shell.py       # 反弹 Shell/Base64 生成
└── utils/
    ├── helpers.py              # 字体加载 (原 get_loacl_font)、ASCII 艺术
    └── logger.py               # 统一日志
```

**数据流**：`MainWindow` → 下拉列表选择 → 懒加载对应 `ui/pages/*.py` → 用户输入 → 调用 `tools/*.py` → 回调更新 `result_area`。

**旧文件**（`Fun*.py`, `Get*.py`）保留用于向后兼容，新代码不再依赖它们。

## Code Style

- 所有文件 UTF-8 + `# -*- coding: utf-8 -*-`，中文注释和字符串普遍存在
- 公开函数：`snake_case`（如 `save_dns_records_to_log`, `get_menu_links`）
- 类名：`PascalCase`（如 `MainWindow`, `NmapPage`, `DnsPage`）
- 槽函数：`on_` 前缀（如 `_on_tool_changed`, `_on_scan`）
- 模块文件：新模块用 `snake_case`（如 `nmap_scanner.py`, `dns_lookup.py`）；旧模块保留 `Get`/`Fun` 前缀 + PascalCase
- 实例变量：`snake_case`（如 `self.result_area`, `self.tool_combo`）

## PyQt6 Patterns

- **控件工厂**：`ui/widgets.py` 提供 `create_label/input/output/button`，页面通过 `layout.addWidget(widget, row, col, rowspan, colspan)` 布局。
- **Placeholder 实现**：`QLineEdit.focusInEvent/focusOutEvent` monkey-patch 实现（`widgets.py` 内），非子类化。
- **工具页面**：每个工具一个 `ui/pages/*.py`，继承 `QWidget`，通过 `status_callback` 和 `result_callback` 与主窗口通信。
- **懒加载**：`MainWindow._get_or_create_page()` 按需创建页面并缓存。
- **样式**：全局 `app.setStyleSheet(darkcss())` + `ui/theme.py`。
- **线程**：`cmd_page.py` 使用 `threading.Thread(daemon=True)` + `QTimer(50ms)` 异步执行命令。
- **菜单**：`config/links.py` 的 `get_menu_links()` 返回 3 个字典元组，索引 `[0]/[1]/[2]` 访问。

## Gotchas

1. **Lambda 闭包陷阱**：菜单链接回调用 `lambda checked, u=url: webbrowser.open(u)`（默认参数捕获），不要简化为 `lambda: webbrowser.open(url)`。
2. **工具页面添加**：新增工具需要 ① `tools/` 下写逻辑 ② `ui/pages/` 下写面板 ③ `MainWindow._get_or_create_page()` 注册。
3. **无外部配置文件**：所有配置在 `config/settings.py` 和 `config/links.py` 中。
4. **日志目录**：运行时在项目根目录创建 `UserLog/`，已加入 `.gitignore`。
5. **字体**：优先加载本地 `SarasaFixedSC-Light.ttf`，失败时回退 `Consolas`。
