# -*- coding: utf-8 -*-
"""WHOIS 查询页面"""

from PyQt6.QtWidgets import QWidget, QGridLayout
from ui.widgets import create_label, create_input, create_button
from tools.whois_query import whois_txt
from config.settings import DEFAULT_WHOIS_SERVER


class WhoisPage(QWidget):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)

        layout = QGridLayout(self)

        layout.addWidget(create_label("WHOIS 查询"), 0, 0, 1, 5)

        self.input_domain = create_input("输入域名或 IP")
        layout.addWidget(self.input_domain, 1, 0, 1, 2)

        self.input_server = create_input(f"WHOIS 服务器 (默认 {DEFAULT_WHOIS_SERVER})")
        layout.addWidget(self.input_server, 1, 2, 1, 2)

        btn = create_button("查询")
        btn.clicked.connect(self._on_query)
        layout.addWidget(btn, 1, 4)

    def _on_query(self):
        domain = self.input_domain.text().strip()
        server = self.input_server.text().strip() or DEFAULT_WHOIS_SERVER
        try:
            result, logpath = whois_txt(domain, server)
            self.result_callback(result)
            self.status_callback(logpath)
        except Exception as e:
            self.result_callback(f"Error: {e}")
