# -*- coding: utf-8 -*-
"""用户设置对话框"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox,
)

from config.settings import COLORS
from utils.settings_manager import get_proxy, set_proxy, is_proxy_enabled, set_proxy_enabled

C = COLORS


class SettingsDialog(QDialog):
    """用户设置弹窗"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("⚙ 设置")
        self.setFixedSize(480, 280)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {C["bg_primary"]};
                color: {C["text_primary"]};
            }}
            QLabel {{
                background: transparent;
                border: none;
            }}
            QLineEdit {{
                background-color: {C["bg_card"]};
                border: 1px solid {C["border"]};
                border-radius: 6px;
                color: {C["text_primary"]};
                padding: 8px 12px;
                font-size: 13px;
                min-height: 36px;
            }}
            QLineEdit:focus {{
                border-color: {C["accent"]};
            }}
            QPushButton {{
                background-color: {C["bg_card"]};
                color: {C["accent"]};
                border: 1px solid {C["border"]};
                border-radius: 6px;
                padding: 8px 18px;
                font-size: 13px;
                font-weight: bold;
                min-height: 36px;
            }}
            QPushButton:hover {{
                background-color: {C["bg_hover"]};
                border-color: {C["accent"]};
            }}
            QPushButton#save_btn {{
                background-color: {C["accent"]};
                color: {C["bg_primary"]};
                border: none;
            }}
            QPushButton#save_btn:hover {{
                background-color: {C["accent_hover"]};
            }}
            QPushButton#toggle_on {{
                background-color: {C["accent"]};
                color: {C["bg_primary"]};
                border: none;
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                font-weight: bold;
                min-height: 28px;
            }}
            QPushButton#toggle_on:hover {{
                background-color: {C["accent_hover"]};
            }}
            QPushButton#toggle_off {{
                background-color: transparent;
                color: {C["text_secondary"]};
                border: 1px solid {C["border"]};
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 12px;
                min-height: 28px;
            }}
            QPushButton#toggle_off:hover {{
                color: {C["text_primary"]};
                border-color: {C["text_primary"]};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # 代理设置
        header = QHBoxLayout()
        title = QLabel("网络代理")
        title.setStyleSheet(f"color: {C['accent']}; font-size: 14px; font-weight: bold;")
        header.addWidget(title)
        header.addStretch()

        # 启用 / 禁用 切换按钮
        self._enabled = is_proxy_enabled()
        self.btn_on = QPushButton("● 启用")
        self.btn_off = QPushButton("○ 禁用")
        self.btn_on.setObjectName("toggle_on" if self._enabled else "toggle_off")
        self.btn_off.setObjectName("toggle_on" if not self._enabled else "toggle_off")
        self.btn_on.clicked.connect(lambda: self._toggle(True))
        self.btn_off.clicked.connect(lambda: self._toggle(False))
        header.addWidget(self.btn_on)
        header.addWidget(self.btn_off)
        layout.addLayout(header)

        desc = QLabel("用于下载弱口令字典等需要外网的场景\n格式: 127.0.0.1:7897（不含 http://）")
        desc.setStyleSheet(f"color: {C['text_secondary']}; font-size: 12px;")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        proxy_row = QHBoxLayout()
        proxy_row.setSpacing(10)

        self.proxy_input = QLineEdit()
        self.proxy_input.setPlaceholderText("如 127.0.0.1:7897")
        self.proxy_input.setText(get_proxy())
        self.proxy_input.setEnabled(self._enabled)
        proxy_row.addWidget(self.proxy_input, stretch=1)

        self.save_btn = QPushButton("保存")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self._on_save)
        self.save_btn.setEnabled(True)
        proxy_row.addWidget(self.save_btn)

        layout.addLayout(proxy_row)

        # 底部提示
        layout.addStretch()
        hint = QLabel("修改后立即生效，需重启应用才能应用到已运行的模块")
        hint.setStyleSheet(f"color: {C['text_secondary']}; font-size: 11px;")
        hint.setWordWrap(True)
        layout.addWidget(hint)

    def _toggle(self, enabled: bool):
        """切换代理启用/禁用状态"""
        self._enabled = enabled
        self.proxy_input.setEnabled(enabled)
        self.btn_on.setObjectName("toggle_on" if enabled else "toggle_off")
        self.btn_off.setObjectName("toggle_on" if not enabled else "toggle_off")
        # 刷新样式
        for btn in [self.btn_on, self.btn_off]:
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def _on_save(self):
        if self._enabled:
            value = self.proxy_input.text().strip()
            if not value:
                self._msg("错误", "代理地址不能为空", "warning")
                return
            set_proxy(value)
            set_proxy_enabled(True)
            self._msg("成功", f"代理已启用: {value}", "info")
        else:
            set_proxy_enabled(False)
            self._msg("成功", "代理已禁用", "info")
        self.accept()

    def _msg(self, title: str, text: str, level: str):
        """显示自定义样式的消息框（适配暗色主题）"""
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(text)
        # QMessageBox 是独立窗口，不继承 Dialog 样式，需显式指定
        box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {C["bg_primary"]};
                color: {C["text_primary"]};
            }}
            QLabel {{
                color: {C["text_primary"]};
                font-size: 13px;
                background: transparent;
            }}
            QPushButton {{
                background-color: {C["bg_card"]};
                color: {C["accent"]};
                border: 1px solid {C["border"]};
                border-radius: 4px;
                padding: 6px 16px;
                min-width: 64px;
            }}
            QPushButton:hover {{
                background-color: {C["bg_hover"]};
            }}
        """)
        if level == "warning":
            box.setIcon(QMessageBox.Icon.Warning)
        else:
            box.setIcon(QMessageBox.Icon.Information)
        box.exec()
