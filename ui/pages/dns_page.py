# -*- coding: utf-8 -*-
"""DNS 记录查询页面"""

from PyQt6.QtWidgets import QWidget, QGridLayout
from ui.widgets import create_label, create_input, create_button
from tools.dns_lookup import save_dns_records_to_log
from config.settings import DEFAULT_DNS_SERVER


class DnsPage(QWidget):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)

        layout = QGridLayout(self)

        layout.addWidget(create_label("DNS 记录查询"), 0, 0, 1, 5)

        self.input_domain = create_input("输入域名")
        layout.addWidget(self.input_domain, 1, 0, 1, 2)

        self.input_dns = create_input(f"DNS 服务器 (默认 {DEFAULT_DNS_SERVER})")
        layout.addWidget(self.input_dns, 1, 2, 1, 2)

        btn = create_button("查询")
        btn.clicked.connect(self._on_query)
        layout.addWidget(btn, 1, 4)

    def _on_query(self):
        domain = self.input_domain.text().strip()
        dns_server = self.input_dns.text().strip() or DEFAULT_DNS_SERVER
        try:
            content, logpath = save_dns_records_to_log(domain, dns_server)
            self.result_callback(content)
            self.status_callback(f"DNS logpath: {logpath}")
        except Exception as e:
            self.result_callback(f"Error: {e}")
