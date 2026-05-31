# -*- coding: utf-8 -*-
"""可复用的 PyQt6 控件工厂"""

from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt


def create_label(text: str) -> QLabel:
    """创建紧凑橙色标题标签"""
    label = QLabel(text)
    label.setFixedHeight(24)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
    label.setStyleSheet("padding: 2px 8px;")
    return label


def create_title(text: str) -> QLabel:
    """创建工具页面标题（无背景拉伸）"""
    label = QLabel(text)
    label.setStyleSheet("""
        QLabel {
            background-color: transparent;
            color: #CD661D;
            font-size: 14px;
            font-weight: bold;
            padding: 4px 0;
            border: none;
        }
    """)
    return label


def create_input(placeholder: str) -> QLineEdit:
    """创建带 placeholder 提示的输入框（使用原生 setPlaceholderText）"""
    input_field = QLineEdit()
    input_field.setPlaceholderText(placeholder)
    input_field.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
    return input_field


def create_output(placeholder: str = "", readonly: bool = True) -> QTextEdit:
    """创建只读输出区域"""
    textarea = QTextEdit(placeholder)
    textarea.setReadOnly(readonly)
    return textarea


def create_button(text: str) -> QPushButton:
    """创建按钮"""
    return QPushButton(text)
