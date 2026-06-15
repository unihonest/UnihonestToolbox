#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import sys
import webbrowser

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QTextEdit, QMenu, QLabel, QStackedWidget, QSizePolicy,
)
from PySide6.QtGui import QAction

from config.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, NAV_ITEMS,
)
from config.links import get_menu_links
from ui.theme import darkcss
from ui.tool_text import get_tool_txt
from ui.widgets import create_nav_button
from ui.settings_dialog import SettingsDialog
from ui.pages.nmap_page import NmapPage
from ui.pages.dns_page import DnsPage
from ui.pages.whois_page import WhoisPage
from ui.pages.password_page import PasswordPage
from ui.pages.ip_page import IpPage
from ui.pages.ip_lookup_page import IpLookupPage
from utils.helpers import load_mono_font, get_figlet_art

# 工具注册表：{名称: PageClass}
TOOL_REGISTRY = {
    "Nmap": NmapPage,
    "Whois": WhoisPage,
    "DNS-type": DnsPage,
    "弱口令检测": PasswordPage,
    "IP计算器": IpPage,
    "公网IP查询": IpLookupPage,
}

class MainWindow(QMainWindow):
    """网络安全工具箱主窗口 — 侧边栏导航 + 堆叠页面"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.statusBar().showMessage("🟢 就绪")

        # ── 菜单栏 ──
        self._build_menubar()

        # 菜单栏最右侧：设置（下拉菜单，保持可扩展性）
        settings_menu = self.menuBar().addMenu("设置")
        proxy_action = QAction("代理设置", self)
        proxy_action.triggered.connect(self._on_settings)
        settings_menu.addAction(proxy_action)

        # ── 中央部件：侧边栏 + 右侧内容 ──
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── 左侧边栏 ──
        side_bar = QWidget()
        side_bar.setObjectName("side_bar")
        side_layout = QVBoxLayout(side_bar)
        side_layout.setContentsMargins(0, 12, 0, 0)
        side_layout.setSpacing(0)

        # 导航按钮组
        self.nav_buttons = {}
        for icon, name in NAV_ITEMS:
            btn = create_nav_button(icon, name)
            btn.clicked.connect(lambda checked, n=name: self._on_nav(n))
            side_layout.addWidget(btn)
            self.nav_buttons[name] = btn

        side_layout.addStretch()

        # 版本号
        side_version = QLabel("v2.0")
        side_version.setObjectName("side_version")
        side_layout.addWidget(side_version)

        root.addWidget(side_bar)

        # ── 右侧内容区：描述 → 输入 → 输出 ──
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(20, 12, 20, 12)
        right_panel.setSpacing(8)

        # ① 工具描述区
        self.tool_desc = QLabel("")
        self.tool_desc.setObjectName("tool_desc")
        self.tool_desc.setWordWrap(True)
        self.tool_desc.setMaximumHeight(48)
        right_panel.addWidget(self.tool_desc)

        # ② 工具输入区
        self.stack = QStackedWidget()
        self.stack.setObjectName("input_stack")
        self.stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self._pages = {}
        right_panel.addWidget(self.stack)

        # ③ 工具输出区
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setFont(load_mono_font(13))
        self.result_area.setText(get_figlet_art("unihonest"))
        right_panel.addWidget(self.result_area, stretch=1)

        root.addLayout(right_panel, stretch=1)

        # ── 默认选中第一个工具 ──
        if NAV_ITEMS:
            self._on_nav(NAV_ITEMS[0][1])

    # ── 菜单栏构建 ──
    def _build_menubar(self):
        pentest, incident, news = get_menu_links()
        menu_data = [
            ("渗透测试", pentest),
            ("应急响应", incident),
            ("新闻资讯", news),
        ]

        for menu_title, data in menu_data:
            main_menu = self.menuBar().addMenu(menu_title)
            for submenu_title, actions in data[menu_title]:
                sub_menu = QMenu(submenu_title, self)
                for name, url in actions:
                    action = QAction(name, self)
                    action.triggered.connect(lambda checked, u=url: webbrowser.open(u))
                    action.setStatusTip(url)
                    sub_menu.addAction(action)
                main_menu.addMenu(sub_menu)

    # ── 侧边栏导航 ──
    def _on_nav(self, name: str):
        """导航按钮点击：切换页面 + 更新描述 + 高亮按钮"""
        # 更新导航按钮高亮
        for btn_name, btn in self.nav_buttons.items():
            btn.setProperty("active", btn_name == name)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        # 更新工具描述
        try:
            desc = get_tool_txt(name)
            # 取第一行作为简短描述，排除标题行
            lines = [l for l in desc.strip().split("\n") if l.strip() and not l.startswith("举")]
            summary = lines[0] if lines else ""
            self.tool_desc.setText(summary)
        except Exception:
            self.tool_desc.setText("")

        # 切换页面
        page = self._get_or_create_page(name)
        if page:
            self.stack.setCurrentWidget(page)

    # ── 页面懒加载 ──
    def _get_or_create_page(self, name: str):
        """懒加载工具页面（配置驱动）"""
        if name in self._pages:
            return self._pages[name]

        PageClass = TOOL_REGISTRY.get(name)
        if not PageClass:
            return None

        page = PageClass(
            status_callback=self.statusBar().showMessage,
            result_callback=self.result_area.setText,
        )
        self._pages[name] = page
        self.stack.addWidget(page)
        return page

    # ── 设置按钮 ──
    def _on_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()



def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(darkcss())
    app.setFont(load_mono_font(13))

    window = MainWindow()
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
