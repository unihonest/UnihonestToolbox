# -*- coding: utf-8 -*-
"""密码强度检测页面"""

from PyQt6.QtWidgets import QWidget, QGridLayout
from ui.widgets import create_label, create_input, create_button
from tools.password_checker import check_password_strength, check_password_batch, download_full_wordlist


class PasswordPage(QWidget):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)

        layout = QGridLayout(self)

        layout.addWidget(create_label("密码强度分析 - 支持批量，用换行分割"), 0, 0, 1, 5)

        self.input_pwd = create_input("输入密码（多个密码请用换行分割）")
        layout.addWidget(self.input_pwd, 1, 0, 1, 2)

        btn_check = create_button("检测强度")
        btn_check.clicked.connect(self._on_check_strength)
        layout.addWidget(btn_check, 1, 2)

        btn_batch = create_button("批量检测")
        btn_batch.clicked.connect(self._on_check_batch)
        layout.addWidget(btn_batch, 1, 3)

        btn_download = create_button("下载完整字典")
        btn_download.clicked.connect(self._on_download)
        layout.addWidget(btn_download, 1, 4)

    def _on_check_strength(self):
        pwd = self.input_pwd.text().strip()
        if "\n" in pwd:
            self.result_callback("检测到多个密码，请点击「批量检测」按钮")
            return
        result = check_password_strength(pwd)
        self.result_callback(result)

    def _on_check_batch(self):
        text = self.input_pwd.text().strip()
        result = check_password_batch(text)
        self.result_callback(result)

    def _on_download(self):
        self.result_callback("正在下载 SecLists Top 10000 完整字典...")
        msg, count = download_full_wordlist()
        self.result_callback(msg)
        if count > 0:
            self.status_callback(f"字典已安装 ({count} 条)")
