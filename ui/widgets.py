# -*- coding: utf-8 -*-
"""可复用的 PySide6 控件工厂"""

from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import Qt


def create_label(text: str) -> QLabel:
    """创建工具页面标题标签（青蓝、左对齐、无背景）"""
    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    label.setStyleSheet(
        "color: #4fc3f7; font-size: 14px; font-weight: bold; "
        "background: transparent; border: none; padding: 4px 0;"
    )
    return label


def create_input(placeholder: str) -> QLineEdit:
    """创建带 placeholder 提示的输入框"""
    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder)
    input_field.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    return input_field


def create_button(text: str) -> QPushButton:
    """创建操作按钮"""
    return QPushButton(text)


def create_nav_button(icon: str, text: str) -> QPushButton:
    """创建侧边栏导航按钮：图标 + 文字，左对齐"""
    btn = QPushButton(f"  {icon}  {text}")
    btn.setObjectName("nav_btn")
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setProperty("active", False)
    return btn


class BasePage(QWidget):
    """工具页面基类：统一 callback 和 layout 初始化"""

    def __init__(self, status_callback=None, result_callback=None):
        super().__init__()
        self.status_callback = status_callback or (lambda msg: None)
        self.result_callback = result_callback or (lambda text: None)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 8, 0, 8)
        self.layout.setVerticalSpacing(8)
        self.layout.setHorizontalSpacing(8)
