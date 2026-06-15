# -*- coding: utf-8 -*-
"""辅助工具：字体加载、ASCII 艺术字等"""

import os
import pyfiglet
from PySide6.QtGui import QFont, QFontDatabase


def load_mono_font(size: int = 13):
    """加载本地更纱黑体等宽字体（用于输出区域），失败则回退 Consolas"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(current_dir, "font", "SarasaFixedSC-Light.ttf")

    if not os.path.exists(font_path):
        return QFont("Consolas", size)

    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        return QFont("Consolas", size)

    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        return QFont("Consolas", size)

    return QFont(families[0], size)


def get_figlet_art(text: str, font: str = "univers", width: int = 100) -> str:
    """生成 ASCII 艺术字"""
    figlet = pyfiglet.Figlet(font=font, width=width)
    return figlet.renderText(text)
