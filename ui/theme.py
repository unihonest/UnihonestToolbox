# -*- coding: utf-8 -*-
"""现代深色科技风 QSS 主题 — 适配 2560×1440"""

from config.settings import COLORS

C = COLORS  # shorthand


def darkcss() -> str:
    return f"""
        /* ═══════════════════════════════════════════
           全局
           ═══════════════════════════════════════════ */
        * {{
            font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
            font-size: 13px;
        }}

        QMainWindow {{
            background-color: {C["bg_primary"]};
        }}

        /* ═══════════════════════════════════════════
           菜单栏
           ═══════════════════════════════════════════ */
        QMenuBar {{
            background-color: {C["bg_secondary"]};
            color: {C["text_primary"]};
            border-bottom: 1px solid {C["border"]};
            padding: 2px 0;
        }}
        QMenuBar::item {{
            padding: 6px 14px;
            background: transparent;
            border-radius: 4px;
            margin: 2px 4px;
        }}
        QMenuBar::item:selected {{
            background-color: {C["bg_hover"]};
        }}
        QMenu {{
            background-color: {C["bg_secondary"]};
            border: 1px solid {C["border"]};
            border-radius: 6px;
            padding: 4px;
            color: {C["text_primary"]};
        }}
        QMenu::item {{
            padding: 6px 28px 6px 16px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: {C["accent"]};
            color: {C["bg_primary"]};
        }}
        QMenu::separator {{
            height: 1px;
            background: {C["border"]};
            margin: 4px 8px;
        }}

        /* ═══════════════════════════════════════════
           侧边栏
           ═══════════════════════════════════════════ */
        QWidget#side_bar {{
            background-color: {C["bg_secondary"]};
            border-right: 1px solid {C["border"]};
            min-width: {C["sidebar_width"]}px;
            max-width: {C["sidebar_width"]}px;
        }}
        QLabel#side_version {{
            color: {C["text_secondary"]};
            font-size: 11px;
            padding: 8px 14px;
            background: transparent;
            border: none;
        }}

        /* ═══════════════════════════════════════════
           导航按钮
           ═══════════════════════════════════════════ */
        QPushButton#nav_btn {{
            background-color: transparent;
            color: {C["text_secondary"]};
            border: none;
            border-left: 3px solid transparent;
            text-align: left;
            padding: 10px 14px;
            font-size: 13px;
            border-radius: 0;
        }}
        QPushButton#nav_btn:hover {{
            background-color: {C["bg_hover"]};
            color: {C["text_primary"]};
            border-left: 3px solid {C["bg_hover"]};
        }}
        QPushButton#nav_btn[active="true"] {{
            background-color: {C["bg_card"]};
            color: {C["accent"]};
            border-left: 3px solid {C["accent"]};
            font-weight: bold;
        }}

        /* ═══════════════════════════════════════════
           工具描述区
           ═══════════════════════════════════════════ */
        QLabel#tool_desc {{
            color: {C["text_primary"]};
            font-size: 12px;
            padding: 8px 12px;
            background-color: {C["bg_card"]};
            border: 1px solid {C["border"]};
            border-left: 3px solid {C["accent"]};
            border-radius: 4px;
        }}

        /* ═══════════════════════════════════════════
           输入堆叠区
           ═══════════════════════════════════════════ */
        QStackedWidget#input_stack {{
            background-color: {C["bg_card"]};
            border: 1px solid {C["border"]};
            border-radius: 6px;
            padding: 4px;
        }}

        /* ═══════════════════════════════════════════
           输入框
           ═══════════════════════════════════════════ */
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
        QLineEdit:hover:!focus {{
            border-color: {C["bg_hover"]};
        }}

        /* ═══════════════════════════════════════════
           按钮
           ═══════════════════════════════════════════ */
        QPushButton:!QPushButton#nav_btn {{
            background-color: {C["bg_card"]};
            color: {C["accent"]};
            border: 1px solid {C["border"]};
            border-radius: 6px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: bold;
            min-height: 36px;
        }}
        QPushButton:!QPushButton#nav_btn:hover {{
            background-color: {C["bg_hover"]};
            border-color: {C["accent"]};
        }}
        QPushButton:!QPushButton#nav_btn:pressed {{
            background-color: {C["accent"]};
            color: {C["bg_primary"]};
        }}
        QPushButton:!QPushButton#nav_btn:disabled {{
            background-color: {C["bg_card"]};
            color: {C["text_secondary"]};
            border-color: {C["border"]};
        }}

        /* ═══════════════════════════════════════════
           输出区域
           ═══════════════════════════════════════════ */
        QTextEdit {{
            background-color: {C["bg_card"]};
            border: 1px solid {C["border"]};
            border-radius: 6px;
            color: {C["text_primary"]};
            padding: 10px;
            font-family: "Sarasa Fixed SC", "Consolas", "Courier New", monospace;
            font-size: 13px;
        }}
        QTextEdit:focus {{
            border-color: {C["accent"]};
        }}

        /* ═══════════════════════════════════════════
           下拉框
           ═══════════════════════════════════════════ */
        QComboBox {{
            background-color: {C["bg_card"]};
            border: 1px solid {C["border"]};
            border-radius: 6px;
            color: {C["text_primary"]};
            padding: 8px 12px;
            min-height: 36px;
        }}
        QComboBox:hover {{
            border-color: {C["accent"]};
        }}
        QComboBox QAbstractItemView {{
            background-color: {C["bg_secondary"]};
            color: {C["text_primary"]};
            border: 1px solid {C["border"]};
            border-radius: 4px;
            selection-background-color: {C["accent"]};
            selection-color: {C["bg_primary"]};
            outline: none;
        }}
        QComboBox QAbstractItemView::item {{
            padding: 6px 12px;
            min-height: 28px;
        }}

        /* ═══════════════════════════════════════════
           状态栏
           ═══════════════════════════════════════════ */
        QStatusBar {{
            background-color: {C["bg_secondary"]};
            color: {C["text_secondary"]};
            border-top: 1px solid {C["border"]};
            font-size: 11px;
            padding: 2px 8px;
        }}
        QStatusBar::item {{
            border: none;
        }}

        /* ═══════════════════════════════════════════
           滚动条
           ═══════════════════════════════════════════ */
        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {C["border"]};
            min-height: 24px;
            border-radius: 4px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {C["accent"]};
        }}
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar:horizontal {{
            background: transparent;
            height: 8px;
            margin: 0;
        }}
        QScrollBar::handle:horizontal {{
            background: {C["border"]};
            min-width: 24px;
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {C["accent"]};
        }}
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0;
        }}

        /* ═══════════════════════════════════════════
           GroupBox
           ═══════════════════════════════════════════ */
        QGroupBox {{
            border: 1px solid {C["border"]};
            border-radius: 6px;
            margin-top: 12px;
            padding: 16px 12px 12px 12px;
            color: {C["text_primary"]};
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
            color: {C["accent"]};
        }}

        /* ═══════════════════════════════════════════
           分隔线
           ═══════════════════════════════════════════ */
        QFrame#separator {{
            background-color: {C["border"]};
            max-height: 1px;
            margin: 4px 0;
        }}

        /* ═══════════════════════════════════════════
           工具提示
           ═══════════════════════════════════════════ */
        QToolTip {{
            background-color: {C["bg_card"]};
            color: {C["text_primary"]};
            border: 1px solid {C["accent"]};
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 12px;
        }}
    """
