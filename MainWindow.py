#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QComboBox,
    QFrame, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QMenu
)
from PyQt6.QtCore import QTimer, QUrl, Qt
from PyQt6.QtGui import QFont, QDesktopServices, QAction, QFontDatabase
import sys
import os
import subprocess
import threading
import platform
import webbrowser
from FunNmapScanner import NmapScan
from FunDNSType import save_dns_records_to_log
from FunWhoisInfo import whois_txt
from GetDarkCSS import darkcss
from GetMenubarLink import get_manu_link
from GetToolTXT import get_tool_txt
from GetNewsLink import get_news_link

def get_loacl_font():
    current_dir = os.path.dirname(os.path.abspath(__file__)) # 确定字体文件路径
    font_path = os.path.join(current_dir, "SarasaFixedSC-TTF-1.0.24", "SarasaFixedSC-Light.ttf")
    if not os.path.exists(font_path): # 检查字体文件是否存在
        print(f"Font file not found at: {font_path}")
        return QFont("Consolas", 11)
    
    font_id = QFontDatabase.addApplicationFont(font_path) # 加载本地字体文件
    if font_id < 0:
        print("Failed to add application font.")
        return QFont("Consolas", 11)
    
    families = QFontDatabase.applicationFontFamilies(font_id) # 获取字体家族名称
    if not families:
        print("No available font families in the loaded font.")
        return QFont("Consolas", 11)

    # 使用加载的字体创建 QFont 对象
    return QFont(families[0], 11)  # 选择第一个可用的字体家族，并指定字体大小


# QT6的QMainWindow实例
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = None                             # 保存子进程引用
        self.is_running = False                         # 标记命令是否正在运行

        self.setWindowTitle("网络安全工具箱 - unihonest")       # 设置窗口标题
        self.statusBar().showMessage('StatusBar')          # 设置底部状态栏
        
        scroll_area = QScrollArea()                     # 创建可滚动区域
        self.setCentralWidget(scroll_area)              # 设置为中心部件
        scroll_area.setWidgetResizable(True)            # 允许自动调整子部件大小

        content_widget = QFrame()                       # 创建内容框架
        scroll_area.setWidget(content_widget)           # 设置滚动区域的子部件

        main_layout = QVBoxLayout()                     # 使用垂直布局作为主布局
        content_widget.setLayout(main_layout)           # 设置主布局到框架

        grid_layout = QGridLayout()                     # 创建网格布局
        main_layout.addLayout(grid_layout)              # 添加到主布局中

        # 创建通用组件添加函数，QLabel，QLineEdit，QTextEdit，QPushButton, QMenu
        def add_label(text, row, col, row_span=1, col_span=5):
            label = QLabel(text)
            grid_layout.addWidget(label, row, col, row_span, col_span)

        def add_input(placeholder, row, col, row_span=1, col_span=2):
            def on_focus_in(event):
                if input_field.text() == placeholder:
                    input_field.clear()
                QLineEdit.focusInEvent(input_field, event)  # 调用父类方法

            def on_focus_out(event):
                if not input_field.text():
                    input_field.setText(placeholder)
                QLineEdit.focusOutEvent(input_field, event)  # 调用父类方法

            input_field = QLineEdit(placeholder)
            grid_layout.addWidget(input_field, row, col, row_span, col_span)
            input_field.setFocusPolicy(Qt.FocusPolicy.StrongFocus) # 连接 focusIn 和 focusOut 事件
            input_field.focusInEvent = on_focus_in
            input_field.focusOutEvent = on_focus_out

            return input_field

        def add_textarea(placeholder, row, col, row_span=1, col_span=2):
            textarea = QTextEdit(placeholder)
            grid_layout.addWidget(textarea, row, col, row_span, col_span)
            textarea.setReadOnly(True)
            return textarea

        def add_button(text, row, col, row_span=1, col_span=1):
            button = QPushButton(text)
            grid_layout.addWidget(button, row, col, row_span, col_span)
            return button

        def add_menu_with_actions(parent_menu, menu_title, actions):
            """Helper function to create a menu with its actions."""
            menu = QMenu(menu_title, self)
            for action_name, url in actions:
                action = QAction(action_name, self)
                action.triggered.connect(lambda checked, u=url: webbrowser.open(u))
                menu.addAction(action)
                action.setStatusTip(url)
            parent_menu.addMenu(menu)
            return menu

        # 创建菜单栏
        menubar = self.menuBar()
        grid_layout.addWidget(menubar, 0, 4)  # 设置菜单栏位置
        menubar.setFixedWidth(100)  # 固定菜单栏列宽

        # 从MenubarLink.py获取链接
        menus_and_actions_link = get_manu_link()

        # 添加主菜单
        main_menu = menubar.addMenu('安全链接')

        # 添加子菜单和动作
        for submenu_title, submenu_actions in menus_and_actions_link['安全链接']:
            add_menu_with_actions(main_menu, submenu_title, submenu_actions)

        # 创建安全新闻的 QComboBox 控件
        self.combo1 = QComboBox(self)
        self.news_link = get_news_link()
        for news in self.news_link:
            self.combo1.addItem(news[0])  # 添加新闻源名称到下拉菜单

        self.combo1.currentTextChanged.connect(self.on_combobox_changed) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo1, 0, 0)

        # 创建安全工具的 QComboBox 控件
        self.combo2 = QComboBox(self)
        self.combo2.addItems(['安全工具', 'OneForAll'])
        self.combo2.currentTextChanged.connect(self.on_combobox_ToolTXT) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo2, 0, 1)

        # 创建自写工具的 QComboBox 控件
        self.combo3 = QComboBox(self)
        self.combo3.addItems(['自写工具', 'Nmap', 'Whois', 'DNS-type'])
        self.combo3.currentTextChanged.connect(self.on_combobox_ToolTXT) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo3, 1, 0, 1, 5)
        self.combo3.setStyleSheet("background-color: #CD661D;")
        
        # 创建自写工具的输入框、功能按钮
        self.unihonest_input1 = add_input("输入框1: 请输入有效参数", 2, 0)
        self.unihonest_input2 = add_input("输入框2: 请输入有效参数", 2, 2)
        scan_button = add_button("Run", 2, 4)
        scan_button.clicked.connect(self.on_button_click)
        

        # Command 控件
        add_label("Command - 在下面的输入框运行一些命令.", 7, 0)
        self.command_input = add_input("Enter command", 8, 0, 1, 3)     
        self.execute_button = add_button("Exec", 8, 3, 1, 1)
        self.execute_button.clicked.connect(self.execute_command)
        self.cancel_button = add_button("Cancel", 8, 4, 1, 1)
        self.cancel_button.clicked.connect(self.cancel_command)
        self.cancel_button.setEnabled(False)                # 初始状态禁用

        # Command Executor 线程锁，缓冲数据
        self.output_lock = threading.Lock()
        self.output_buffer = []
        self.output_timer = QTimer(self)
        self.output_timer.timeout.connect(self.flush_output_buffer)
        self.output_timer.start(50) # 缓冲时间 ms   

        # 结果输出区域
        default_txt = "结果输出区域.\n你可以在 Command 执行其他工具命令。"

        self.result_area = add_textarea(default_txt, 9, 0, 1, 5)
        self.result_area.setText(default_txt)

    # 安全工具的用法文档
    def on_combobox_ToolTXT(self, word_select):
        if word_select == '自写工具':
            self.result_area.setText("自己写的小工具，觉得有用就加进来了。")
            return

        try:
            default_txt = get_tool_txt(word_select)
            self.result_area.setText(default_txt)
            return
        
        except Exception as e:
            self.result_area.setText(f"Error detail: {str(e)}")

    def on_combobox_changed(self, selected_text):
        # 遍历新闻源列表，找到与选择匹配的URL
        for news in self.news_link:
            if news[0] == selected_text:
                url_string = news[1]
                break
        else:
            # 如果没有找到匹配项，默认返回
            self.result_area.setText("未找到对应的新闻链接。")
            return
        
        # 特殊处理 "安全新闻"
        if selected_text == '安全新闻':
            self.result_area.setText("请在“安全新闻”选择一个安全新闻链接。")
            return
             
        # 尝试打开选中的URL
        url = QUrl(url_string)
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open URL', f'Could not open URL: {url_string}')
        else:
            self.result_area.setText(f"正在打开: {url_string}")

    # 自写工具 - 下拉列表 - 传参 - 处理
    def on_button_click(self):
        input1 = str(self.unihonest_input1.text().strip())
        input2 = str(self.unihonest_input2.text().strip())
        if not input1:
            self.result_area.setText("Error: Please enter a valid parameter.")
            return
        
        try:        
            # 检查下拉列表的选择
            selected_item = self.combo3.currentText()
            # 对选择的项目，点击button后的功能处理
            if selected_item == "Nmap":
                try:
                    nmap_table,nm_logpath = NmapScan(input1, input2)
                    self.result_area.setText(nmap_table)
                    self.statusBar().showMessage('Nmap logpath：' + nm_logpath)
                except Exception as e:
                    self.result_area.setText(f"Error detail: {str(e)}")

            elif selected_item == "Whois":
                try:
                    WhoisInfo,logpath3 = whois_txt(input1, input2)
                    self.result_area.setText(WhoisInfo)
                    self.statusBar().showMessage("Whois logpath：" + logpath3)
                except Exception as e:
                    self.result_area.setText(f"Error detail: {str(e)}")
            elif selected_item == "DNS-type":
                try:
                    DnsInfo,logpath2 = save_dns_records_to_log(input1, input2)
                    self.result_area.setText(DnsInfo)
                    self.statusBar().showMessage("DNS logpath：" + logpath2)
                except Exception as e:
                    self.result_area.setText(f"Error detail: {str(e)}")

        except Exception as e:
            self.result_area.setText(f"Error detail: {str(e)}")

    # 命令执行函数
    def execute_command(self):
        if self.is_running:
            return                                              # 如果命令已经在运行，则不执行新命令

        command = self.command_input.text().strip()
        if command:
            self.run_command_in_thread(command)
            self.is_running = True
            self.execute_button.setEnabled(False)                # 禁用执行按钮
            self.cancel_button.setEnabled(True)                  # 启用取消按钮
            self.result_area.setText(command)                    # 清空内容，填入命令

    # 命令执行线程
    def run_command_in_thread(self, command):
        def target():
            try:
                self.process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                )
                while True:
                    line = self.process.stdout.readline()
                    if not line or self.process.poll() is not None:
                        break
                    with self.output_lock:
                        self.output_buffer.append(line.strip())
                # 命令结束后重置状态
                self.reset_state()
            except Exception as e:
                with self.output_lock:
                    self.output_buffer.append(f"Error: {str(e)}")
                self.reset_state()
        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    # 取消命令执行
    def cancel_command(self):
        if self.process and self.process.poll() is None:          # 检查进程是否仍在运行
            self.process.terminate()                              # 发送SIGTERM信号给子进程
            self.process.wait()                                   # 等待进程结束
        self.reset_state()

    # 重置exec、cancel的按钮状态
    def reset_state(self):
        self.is_running = False
        self.execute_button.setEnabled(True)                      # 重新启用执行按钮
        self.cancel_button.setEnabled(False)                      # 禁用取消按钮
        self.statusBar().showMessage('Command run end.')

    # 刷新缓冲的输出
    def flush_output_buffer(self):
        with self.output_lock:
            if self.output_buffer:
                self.result_area.append("\n".join(self.output_buffer)) # 将缓冲的内容添加到结果显示区域
                self.output_buffer.clear()


if __name__ == "__main__":
    # 创建一个 QApplication 实例
    app = QApplication(sys.argv)

    # 设置全局样式
    custom_css = darkcss()
    app.setStyleSheet(custom_css)

    # 设置全局字体
    custom_font = get_loacl_font()
    app.setFont(custom_font)

    # 创建主窗口实例
    window = MainWindow()

    # 调整主窗口的大小
    window.resize(800, 600)

    # 显示主窗口
    window.show()

    # 进入应用程序的主事件循环，等待用户交互，保证干净的退出
    sys.exit(app.exec())