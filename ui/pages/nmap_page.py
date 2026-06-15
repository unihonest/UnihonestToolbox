# -*- coding: utf-8 -*-
"""Nmap 扫描页面 — 异步执行，不阻塞 UI"""

import threading

from PySide6.QtCore import QTimer

from ui.widgets import create_label, create_input, create_button, BasePage
from tools.nmap_scanner import NmapScan


class NmapPage(BasePage):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__(status_callback, result_callback)

        self._scanning = False
        self._scan_done = False
        self._scan_result = None

        # ── 布局 ──
        self.layout.addWidget(create_label("Nmap 扫描"), 0, 0, 1, 5)

        self.input_ip = create_input("输入目标 IP 或域名")
        self.layout.addWidget(self.input_ip, 1, 0, 1, 2)

        self.input_args = create_input("Nmap 参数 (如 -sS -sV -O)")
        self.layout.addWidget(self.input_args, 1, 2, 1, 2)

        self.scan_btn = create_button("扫描")
        self.scan_btn.clicked.connect(self._on_scan)
        self.layout.addWidget(self.scan_btn, 1, 4)

        # ── 轮询定时器：线程完成后更新 UI ──
        self._poll_timer = QTimer(self)
        self._poll_timer.timeout.connect(self._on_poll)

    # ── 扫描入口 ──
    def _on_scan(self):
        if self._scanning:
            return

        ip = self.input_ip.text().strip()
        args = self.input_args.text().strip()

        if not ip:
            self.result_callback("Error: 请输入目标 IP 或域名")
            return

        # 启动异步扫描
        self._scanning = True
        self._scan_done = False
        self._scan_result = None
        self.scan_btn.setEnabled(False)
        self.status_callback("⏳ 正在扫描...")

        def run():
            try:
                self._scan_result = NmapScan(ip, args)
            except Exception as e:
                # 提供更友好的错误提示
                msg = str(e)
                if "Failed to resolve" in msg:
                    msg = f"无法解析目标地址: {ip}"
                elif "Permission denied" in msg or "root privileges" in msg:
                    msg = "权限不足，请以管理员身份运行"
                self._scan_result = (f"Error: {msg}", "")
            finally:
                self._scan_done = True

        threading.Thread(target=run, daemon=True).start()
        self._poll_timer.start(80)

    # ── 轮询结果 ──
    def _on_poll(self):
        if not self._scan_done:
            return

        self._poll_timer.stop()
        self._scanning = False
        self.scan_btn.setEnabled(True)

        result, logpath = self._scan_result or ("Error: 扫描失败", "")
        self.result_callback(result)
        if logpath:
            self.status_callback(f"✅ 扫描完成 — {logpath}")
        else:
            self.status_callback("⚠ 扫描完成（无日志）")
