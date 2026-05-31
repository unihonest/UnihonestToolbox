# -*- coding: utf-8 -*-
"""Nmap 扫描页面"""

from PyQt6.QtWidgets import QWidget, QGridLayout
from ui.widgets import create_label, create_input, create_button
from tools.nmap_scanner import NmapScan


class NmapPage(QWidget):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)

        layout = QGridLayout(self)

        layout.addWidget(create_label("Nmap 扫描"), 0, 0, 1, 5)

        self.input_ip = create_input("输入目标 IP 或域名")
        layout.addWidget(self.input_ip, 1, 0, 1, 2)

        self.input_args = create_input("Nmap 参数 (如 -sS -sV -O)")
        layout.addWidget(self.input_args, 1, 2, 1, 2)

        btn = create_button("扫描")
        btn.clicked.connect(self._on_scan)
        layout.addWidget(btn, 1, 4)

    def _on_scan(self):
        ip = self.input_ip.text().strip()
        args = self.input_args.text().strip()
        try:
            result, logpath = NmapScan(ip, args)
            self.result_callback(result)
            if logpath:
                self.status_callback(f"Nmap logpath: {logpath}")
        except Exception as e:
            self.result_callback(f"Error: {e}")
