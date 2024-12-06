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
            height: 25px;
        }
        QComboBox QAbstractItemView::item:selected {
            background-color: #6A6A6A;
        }
    """
    return dark_style