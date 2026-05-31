# -*- coding: utf-8 -*-
"""命令执行页面"""

import subprocess
import threading

from PyQt6.QtWidgets import QWidget, QGridLayout
from PyQt6.QtCore import QTimer

from ui.widgets import create_label, create_input, create_button


class CmdPage(QWidget):
    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)

        self.process = None
        self.is_running = False
        self.output_lock = threading.Lock()
        self.output_buffer = []

        layout = QGridLayout(self)

        layout.addWidget(create_label("命令执行"), 0, 0, 1, 5)

        self.cmd_input = create_input("输入命令")
        layout.addWidget(self.cmd_input, 1, 0, 1, 3)

        self.btn_exec = create_button("执行")
        self.btn_exec.clicked.connect(self._on_exec)
        layout.addWidget(self.btn_exec, 1, 3)

        self.btn_cancel = create_button("中断")
        self.btn_cancel.clicked.connect(self._on_cancel)
        self.btn_cancel.setEnabled(False)
        layout.addWidget(self.btn_cancel, 1, 4)

        # 缓冲输出定时器
        self.output_timer = QTimer(self)
        self.output_timer.timeout.connect(self._flush_buffer)
        self.output_timer.start(50)

    def _on_exec(self):
        if self.is_running:
            return
        cmd = self.cmd_input.text().strip()
        if not cmd:
            return

        self.is_running = True
        self.btn_exec.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        self.result_callback(cmd)

        def target():
            try:
                self.process = subprocess.Popen(
                    cmd, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True
                )
                for line in iter(self.process.stdout.readline, ""):
                    if self.process.poll() is not None:
                        break
                    with self.output_lock:
                        self.output_buffer.append(line.strip())
                self._reset()
            except Exception as e:
                with self.output_lock:
                    self.output_buffer.append(f"Error: {e}")
                self._reset()

        threading.Thread(target=target, daemon=True).start()

    def _on_cancel(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
        self._reset()

    def _reset(self):
        self.is_running = False
        self.btn_exec.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        self.status_callback("Command run end.")

    def _flush_buffer(self):
        with self.output_lock:
            if self.output_buffer:
                self.result_callback("\n".join(self.output_buffer))
                self.output_buffer.clear()
