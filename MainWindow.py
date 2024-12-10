#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QComboBox,
    QFrame, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QMenu
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QAction, QFontDatabase
import sys
import os
import subprocess
import threading
import webbrowser
import pyfiglet
from FunNmapScanner import NmapScan
from FunDNSType import save_dns_records_to_log
from FunWhoisInfo import whois_txt
from GetDarkCSS import darkcss
from GetMenubarLink import get_manu_link
from GetToolTXT import get_tool_txt

# 加载本地更纱黑体，以绝对路径的方式
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


# 设置艺术字体的样式
def get_figlet_art(text):
    figlet = pyfiglet.Figlet(font='univers', width=120)
    figlet_art = figlet.renderText(text)
    print (figlet_art)
    return figlet_art


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

        # QLabel的创建模板
        def add_label(text, row, col, row_span=1, col_span=5):
            label = QLabel(text)
            grid_layout.addWidget(label, row, col, row_span, col_span)
        
        # QLineEdit的创建模板
        def add_input(placeholder, row, col, row_span=1, col_span=2):
            # 输入时清空默认的文本
            def on_focus_in(event):
                if input_field.text() == placeholder:
                    input_field.clear()
                QLineEdit.focusInEvent(input_field, event)  # 调用父类方法

            # 若未输入内容，则回显默认文本
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

        # QTextEdit的创建模板
        def add_textarea(placeholder, row, col, row_span=1, col_span=2):
            textarea = QTextEdit(placeholder)
            grid_layout.addWidget(textarea, row, col, row_span, col_span)
            textarea.setReadOnly(True)
            return textarea

        # QPushButton的创建模板
        def add_button(text, row, col, row_span=1, col_span=1):
            button = QPushButton(text)
            grid_layout.addWidget(button, row, col, row_span, col_span)
            return button

        # QMenu的创建模板
        def add_menu_with_actions(parent_menu, menu_title, actions):
            """Helper function to create a menu with its actions."""
            menu = QMenu(menu_title, parent_menu.parent())
            for action_name, url in actions:
                action = QAction(action_name, parent_menu.parent())
                action.triggered.connect(lambda checked, u=url: webbrowser.open(u))
                menu.addAction(action)
                action.setStatusTip(url)  # 确保主窗口有状态栏以显示状态提示
            parent_menu.addMenu(menu)
            return menu

        # 创建菜单栏
        menubar = self.menuBar()
        
        # 添加'渗透测试'菜单
        main_menu1 = menubar.addMenu('渗透测试')
        menus_and_actions_link1 = get_manu_link()[0]  # 获取'渗透测试'链接
        
        # 添加子菜单和动作
        for submenu_title1, submenu_actions1 in menus_and_actions_link1['渗透测试']:
            add_menu_with_actions(main_menu1, submenu_title1, submenu_actions1)
        
        # 添加'应急响应'菜单
        main_menu2 = menubar.addMenu('应急响应')
        menus_and_actions_link2 = get_manu_link()[1]  # 获取'应急响应'链接
        
        # 添加子菜单和动作
        for submenu_title2, submenu_actions2 in menus_and_actions_link2['应急响应']:
            add_menu_with_actions(main_menu2, submenu_title2, submenu_actions2)
        
        # 添加'新闻资讯'菜单
        main_menu3 = menubar.addMenu('新闻资讯')
        menus_and_actions_link3 = get_manu_link()[2]  # 获取'应急响应'链接
        
        # 添加子菜单和动作
        for submenu_title3, submenu_actions3 in menus_and_actions_link3['新闻资讯']:
            add_menu_with_actions(main_menu3, submenu_title3, submenu_actions3)

        # “自写工具”的下拉列表
        self.combo3 = QComboBox(self)
        self.combo3.addItems(['自写工具', 'Nmap', 'Whois', 'DNS-type'])
        self.combo3.currentTextChanged.connect(self.on_combobox_ToolTXT) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo3, 1, 0, 1, 5)
        self.combo3.setStyleSheet("background-color: #CD661D;")
        
        # “自写工具”的输入框
        self.unihonest_input1 = add_input("输入框1: 请输入有效参数", 2, 0)
        self.unihonest_input2 = add_input("输入框2: 请输入有效参数", 2, 2)
        scan_button = add_button("运行", 2, 4)
        scan_button.clicked.connect(self.on_button_click)

        # 命令执行 控件
        add_label("命令执行 - 在下面的输入框运行一些命令.", 3, 0)
        self.command_input = add_input("输入命令", 4, 0, 1, 3)     
        self.execute_button = add_button("执行命令", 4, 3, 1, 1)
        self.execute_button.clicked.connect(self.execute_command)
        self.cancel_button = add_button("中断执行", 4, 4, 1, 1)
        self.cancel_button.clicked.connect(self.cancel_command)
        self.cancel_button.setEnabled(False)                # 初始状态禁用

        # Command Executor 线程锁，缓冲数据
        self.output_lock = threading.Lock()
        self.output_buffer = []
        self.output_timer = QTimer(self)
        self.output_timer.timeout.connect(self.flush_output_buffer)
        self.output_timer.start(50) # 缓冲时间 ms   

        # 结果输出区域
        default_txt = get_figlet_art("unihonest")
        self.result_area = add_textarea(default_txt, 5, 0, 1, 5)
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
    window.resize(739, 500)

    # 显示主窗口
    window.show()

    # 进入应用程序的主事件循环，等待用户交互，保证干净的退出
    sys.exit(app.exec())