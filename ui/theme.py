# -*- coding: utf-8 -*-
"""暗色主题 CSS 样式表"""


def darkcss() -> str:
    return """
        QMainWindow {
            background-color: #969696;
            color: #FFFFFF;
        }
        QFrame {
            background-color: #969696;
            color: #FFFFFF;
        }
        QStatusBar {
            background-color: #515151;
            color: #FFFFFF;
            border-radius: 1px;
        }
        QStatusBar::item {
            border: none;
        }
        QLabel {
            background-color: #CD661D;
            border: 1px solid #404040;
            color: #FFFFFF;
            padding: 5px;
            border-radius: 3px;
        }
        QLineEdit {
            background-color: #515151;
            border: 1px solid #404040;
            color: #FFFFFF;
            padding: 5px;
            border-radius: 3px;
        }
        QLineEdit:hover {
            background-color: #6A6A6A;
        }
        QLineEdit:pressed {
            background-color: #3C3C3C;
        }
        QPushButton {
            background-color: #515151;
            border: 1px solid #404040;
            color: #FFFFFF;
            padding: 5px;
            border-radius: 3px;
        }
        QPushButton:hover {
            background-color: #6A6A6A;
        }
        QPushButton:pressed {
            background-color: #3C3C3C;
        }
        QTextEdit {
            background-color: #515151;
            border: 1px solid #404040;
            color: #FFFFFF;
            padding: 5px;
            border-radius: 3px;
        }
        QComboBox {
            background-color: #515151;
            border: 1px solid #404040;
            color: #FFFFFF;
            padding: 5px;
            border-radius: 3px;
        }
        QComboBox QAbstractItemView {
            background-color: #3C3F41;
            color: #FFFFFF;
            selection-background-color: #6A6A6A;
            selection-color: #FFFFFF;
            border: 1px solid #404040;
        }
        QComboBox QAbstractItemView::item {
            height: 30px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #6A6A6A;
        }
        QMenuBar {
            background-color: #515151;
            color: #FFFFFF;
            border-bottom: 1px solid #404040;
        }
        QMenuBar::item {
            padding: 8px 16px;
            background-color: transparent;
            spacing: 3px;
            margin: 0px 4px;
            border-radius: 3px;
        }
        QMenuBar::item:selected {
            background-color: #6A6A6A;
        }
        QMenuBar::item:pressed {
            background-color: #515151;
        }
        QMenu {
            background-color: #515151;
            border: 1px solid #404040;
            color: #FFFFFF;
        }
        QMenu::item {
            padding: 5px 25px 5px 20px;
            border: 1px solid transparent;
            background-color: transparent;
        }
        QMenu::item:selected {
            background-color: #6A6A6A;
        }
        QScrollBar:vertical {
            background: #515151;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #6A6A6A;
            min-height: 20px;
            border-radius: 3px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar:horizontal {
            background: #515151;
            height: 12px;
            margin: 0px;
        }
        QScrollBar::handle:horizontal {
            background: #6A6A6A;
            min-width: 20px;
            border-radius: 3px;
        }
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        QTabWidget::pane {
            border: 1px solid #404040;
            background-color: #969696;
        }
        QTabBar::tab {
            background-color: #515151;
            color: #FFFFFF;
            padding: 8px 16px;
            border: 1px solid #404040;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: #CD661D;
        }
        QTabBar::tab:hover:!selected {
            background-color: #6A6A6A;
        }
        QGroupBox {
            border: 1px solid #404040;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 15px;
            color: #FFFFFF;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #CD661D;
        }
    """
