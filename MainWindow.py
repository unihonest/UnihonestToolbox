#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import sys
import webbrowser

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout,
    QWidget, QTextEdit, QMenu, QComboBox, QHBoxLayout, QLabel,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from config.links import get_menu_links
from ui.theme import darkcss
from ui.tool_text import get_tool_txt
from ui.widgets import create_label
from ui.pages.nmap_page import NmapPage
from ui.pages.dns_page import DnsPage
from ui.pages.whois_page import WhoisPage
from ui.pages.cmd_page import CmdPage
from ui.pages.password_page import PasswordPage
from utils.helpers import load_font, get_figlet_art


class MainWindow(QMainWindow):
    """网络安全工具箱主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.statusBar().showMessage("就绪")

        # ── 菜单栏 ──
        self._build_menubar()

        # ── 中央部件 ──
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # ── 工具选择下拉列表 ──
        top_bar = QHBoxLayout()
        label = QLabel("选择工具")
        label.setStyleSheet("background-color: transparent; border: none; color: #000000; font-weight: bold;")
        top_bar.addWidget(label)
        self.tool_combo = QComboBox()
        self.tool_combo.addItems([
            "自写工具",
            "Nmap", "Whois", "DNS-type", "命令执行", "弱口令检测",
        ])
        self.tool_combo.setStyleSheet("background-color: #CD661D;")
        self.tool_combo.currentTextChanged.connect(self._on_tool_changed)
        top_bar.addWidget(self.tool_combo)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        # ── 标签页（工具面板） ──
        self.tabs = QTabWidget()
        self.tabs.setTabBarAutoHide(True)
        main_layout.addWidget(self.tabs)

        # 工具页面缓存
        self._pages = {}

        # ── 输出区域 ──
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setMinimumHeight(250)
        self.result_area.setText(get_figlet_art("unihonest"))
        main_layout.addWidget(self.result_area)

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

    # ── 工具切换 ──
    def _on_tool_changed(self, name: str):
        if name == "自写工具":
            self.result_area.setText("自己写的小工具，觉得有用就加进来了。")
            return

        # 显示工具说明
        try:
            self.result_area.setText(get_tool_txt(name))
        except Exception:
            pass

        # 切换到对应页面
        page = self._get_or_create_page(name)
        if page:
            idx = self.tabs.indexOf(page)
            if idx < 0:
                idx = self.tabs.addTab(page, name)
            self.tabs.setCurrentIndex(idx)

    def _get_or_create_page(self, name: str):
        """懒加载工具页面"""
        if name in self._pages:
            return self._pages[name]

        page = None
        if name == "Nmap":
            page = NmapPage(
                status_callback=self.statusBar().showMessage,
                result_callback=self.result_area.setText,
            )
        elif name == "Whois":
            page = WhoisPage(
                status_callback=self.statusBar().showMessage,
                result_callback=self.result_area.setText,
            )
        elif name == "DNS-type":
            page = DnsPage(
                status_callback=self.statusBar().showMessage,
                result_callback=self.result_area.setText,
            )
        elif name == "命令执行":
            page = CmdPage(
                status_callback=self.statusBar().showMessage,
                result_callback=self._append_result,
            )
        elif name == "弱口令检测":
            page = PasswordPage(
                status_callback=self.statusBar().showMessage,
                result_callback=self.result_area.setText,
            )

        if page:
            self._pages[name] = page
        return page

    # ── 命令页追加输出（不覆盖） ──
    def _append_result(self, text: str):
        self.result_area.append(text)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(darkcss())
    app.setFont(load_font())

    window = MainWindow()
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
