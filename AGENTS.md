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

侧边栏导航 + QStackedWidget 的现代桌面应用架构。

```
UnihonestToolbox/
├── MainWindow.py              # 入口，侧边栏 + QStackedWidget（TOOL_REGISTRY 配置驱动）
├── config/
│   ├── settings.py            # 窗口/配色/日志/工具列表/导航项
│   └── links.py               # 菜单栏外部链接数据
├── ui/
│   ├── theme.py               # 现代深色科技风 QSS (深蓝底 + 青蓝强调)
│   ├── widgets.py             # 控件工厂 + BasePage + 导航按钮
│   ├── tool_text.py           # 工具使用说明
│   └── pages/                 # 7 个工具面板（继承 BasePage）
├── tools/                     # 业务逻辑层（7 个工具核心）
├── font/
│   └── SarasaFixedSC-Light.ttf
└── utils/
    ├── helpers.py              # 等宽字体加载、ASCII 艺术
    └── logger.py               # 统一日志
```

**数据流**：`MainWindow` → 侧边栏导航点击 → 更新标题 + 懒加载对应 `ui/pages/*.py` → 用户输入 → 调用 `tools/*.py` → 回调更新 `result_area`。

**配色**：`config/settings.py` 的 `COLORS` 字典，主题 `ui/theme.py` 引用。`#1a1a2e` 主背景 / `#4fc3f7` 青蓝强调。

## Code Style

- 所有文件 UTF-8 + `# -*- coding: utf-8 -*-`，中文注释和字符串普遍存在
- 公开函数：`snake_case`（如 `save_dns_records_to_log`, `get_menu_links`）
- 类名：`PascalCase`（如 `MainWindow`, `NmapPage`, `DnsPage`）
- 槽函数：`on_` 前缀（如 `_on_tool_changed`, `_on_scan`）
- 模块文件：用 `snake_case`（如 `nmap_scanner.py`, `dns_lookup.py`）
- 实例变量：`snake_case`（如 `self.result_area`, `self.stack`）

## PySide6 Patterns

- **侧边栏导航**：左侧 200px 深色面板，`create_nav_button(icon, text)` 创建导航按钮，点击切换 `QStackedWidget` 页面。
- **控件工厂**：`ui/widgets.py` 提供 `create_label/input/output/button/nav_button` + `BasePage` 基类。
- **BasePage**：所有工具页面继承 `BasePage`，自动获得 `status_callback`、`result_callback`、`self.layout`（QGridLayout）。
- **工具注册**：`MainWindow.TOOL_REGISTRY` 是 `{显示名: PageClass}` 字典；`NAV_ITEMS` 在 `config/settings.py` 中控制侧边栏图标和顺序。新增工具在两者各加一行即可。
- **样式**：`ui/theme.py` 全局 QSS，配色引用 `config/settings.py` 的 `COLORS` 字典，修改配色只需改一处。
- **字体**：UI 控件用系统字体（Segoe UI / Microsoft YaHei），输出区用等宽字体（Sarasa Fixed SC）。
- **线程**：`nmap_page.py` 使用 `threading.Thread(daemon=True)` + `QTimer(80ms)` 异步执行扫描。
- **菜单**：`config/links.py` 的 `get_menu_links()` 返回 3 个字典元组。

## Gotchas

1. **Lambda 闭包陷阱**：菜单链接回调用 `lambda checked, u=url: webbrowser.open(u)`（默认参数捕获），不要简化为 `lambda: webbrowser.open(url)`。
2. **新增工具流程**：① `tools/` 写逻辑 ② `ui/pages/` 写面板（继承 `BasePage`） ③ `MainWindow.TOOL_REGISTRY` 加一行 ④ `settings.NAV_ITEMS` 加图标+名称。
3. **无外部配置文件**：所有配置在 `config/settings.py` 和 `config/links.py` 中。
4. **日志目录**：运行时在项目根目录创建 `UserLog/`，已加入 `.gitignore`。
5. **字体**：优先加载本地 `SarasaFixedSC-Light.ttf`，失败时回退 `Consolas`。
