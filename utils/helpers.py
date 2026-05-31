# -*- coding: utf-8 -*-
"""辅助工具：字体加载、ASCII 艺术字等"""

import os
import pyfiglet
from PyQt6.QtGui import QFont, QFontDatabase


def load_font():
    """加载本地更纱黑体，失败则回退 Consolas"""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_path = os.path.join(current_dir, "SarasaFixedSC-TTF-1.0.24", "SarasaFixedSC-Light.ttf")

    if not os.path.exists(font_path):
        print(f"Font file not found at: {font_path}")
        return QFont("Consolas", 11)

    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id < 0:
        print("Failed to add application font.")
        return QFont("Consolas", 11)

    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        print("No available font families in the loaded font.")
        return QFont("Consolas", 11)

    return QFont(families[0], 11)


def get_figlet_art(text: str, font: str = "univers", width: int = 120) -> str:
    """生成 ASCII 艺术字"""
    figlet = pyfiglet.Figlet(font=font, width=width)
    return figlet.renderText(text)
