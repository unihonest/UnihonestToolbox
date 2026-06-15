# -*- coding: utf-8 -*-
"""WHOIS 查询页面"""

from ui.widgets import create_label, create_input, create_button, BasePage
from tools.whois_query import whois_txt
from config.settings import DEFAULT_WHOIS_SERVER


class WhoisPage(BasePage):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__(status_callback, result_callback)

        self.layout.addWidget(create_label("WHOIS 查询"), 0, 0, 1, 5)

        self.input_domain = create_input("输入域名或 IP")
        self.layout.addWidget(self.input_domain, 1, 0, 1, 2)

        self.input_server = create_input(f"WHOIS 服务器 (默认 {DEFAULT_WHOIS_SERVER})")
        self.layout.addWidget(self.input_server, 1, 2, 1, 2)

        btn = create_button("查询")
        btn.clicked.connect(self._on_query)
        self.layout.addWidget(btn, 1, 4)

    def _on_query(self):
        domain = self.input_domain.text().strip()
        server = self.input_server.text().strip() or DEFAULT_WHOIS_SERVER
        try:
            result, logpath = whois_txt(domain, server)
            self.result_callback(result)
            self.status_callback(logpath)
        except Exception as e:
            self.result_callback(f"Error: {e}")
