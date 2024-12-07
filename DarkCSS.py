def darkcss():
    dark_style = """
        QMainWindow {
            background-color: #969696;
            color: #FFFFFF;
        }
        QFrame {
            background-color: #969696;
            color: #FFFFFF;
        }
        QLabel {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                         stop:0 #CD661D,
                                         stop:1 #969696);
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
            padding: 5px 15px;
            background-color: transparent;
            spacing: 3px; /* 菜单项之间的间距 */
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
            border: 1px solid transparent; /* 未选中时不显示边框 */
            background-color: transparent;
        }
        QMenu::item:selected { 
            background-color: #6A6A6A;
            border-color: #404040;
        }
        QMenu::icon {
            padding-left: 10px;
        }
        QMenu::separator {
            height: 1px;
            background: #404040;
            margin: 4px 8px;
        }
    """
    return dark_style