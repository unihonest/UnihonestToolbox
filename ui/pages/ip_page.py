# -*- coding: utf-8 -*-
"""IP 子网计算器页面（自动识别 IPv4/IPv6）"""

from ui.widgets import create_label, create_input, create_button, BasePage
from tools.ipv4_calculator import calculate_ipv4
from tools.ipv6_calculator import calculate_ipv6


class IpPage(BasePage):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__(status_callback, result_callback)

        self.layout.addWidget(create_label("IP 子网计算器 (IPv4/IPv6)"), 0, 0, 1, 5)

        self.input_ip = create_input("输入 IP/CIDR，如 192.168.1.1/24 或 2001:db8::1/64")
        self.layout.addWidget(self.input_ip, 1, 0, 1, 4)

        btn = create_button("计算")
        btn.clicked.connect(self._on_calc)
        self.layout.addWidget(btn, 1, 4)

    def _on_calc(self):
        text = self.input_ip.text().strip()
        if ":" in text:
            result = calculate_ipv6(text)
        else:
            result = calculate_ipv4(text)
        self.result_callback(result)
