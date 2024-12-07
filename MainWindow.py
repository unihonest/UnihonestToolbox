#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QComboBox,
    QFrame, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QMenu
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QDesktopServices, QAction
from PyQt6.QtCore import QUrl
import sys
import subprocess
import threading
import platform
import webbrowser
from NmapScanner import NmapScan
from DNSType import save_dns_records_to_log
from WhoisInfo import whois_txt
from DarkCSS import darkcss
from MenubarLink import get_manu_link

# 黑暗风格
dark_style = darkcss()

# 根据系统修改等宽字体，字体大小
def get_system_font():
    system = platform.system().lower()
    if 'linux' in system:
        font_family = QFont("Hack", 6)    # kali linux字体 + 2k hidpi mod
    elif 'windows' in system:
        font_family = QFont("Consolas", 11)
    elif 'darwin' in system:  # macOS
        font_family = QFont("Menlo", 10)
    else:
        font_family = QFont("monospace", 10) # 默认字体，如果无法识别操作系统或者是在一个不常见的操作系统上运行
    
    return font_family


# QT6的QMainWindow实例
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = None                             # 保存子进程引用
        self.is_running = False                         # 标记命令是否正在运行

        self.setWindowTitle("工具箱 - unihonest")       # 设置窗口标题
        self.statusBar().showMessage('Status')          # 设置底部状态栏
        
        font = get_system_font()                        # 设置字体

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
            input_field = QLineEdit(placeholder)
            grid_layout.addWidget(input_field, row, col, row_span, col_span)
            return input_field

        def add_textarea(placeholder, row, col, row_span=1, col_span=2):
            textarea = QTextEdit(placeholder)
            grid_layout.addWidget(textarea, row, col, row_span, col_span)
            textarea.setReadOnly(True)
            textarea.setFont(font)
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
            parent_menu.addMenu(menu)
            return menu

        # 创建菜单栏
        menubar = self.menuBar()
        grid_layout.addWidget(menubar, 0, 4)  # 设置菜单栏位置
        menubar.setFixedWidth(88)  # 固定菜单栏列宽

        # 从MenubarLink.py获取链接
        menus_and_actions_xxsj = get_manu_link()

        # 添加主菜单
        main_menu = menubar.addMenu('安全链接')

        # 添加子菜单和动作
        for submenu_title, submenu_actions in menus_and_actions_xxsj['安全链接']:
            add_menu_with_actions(main_menu, submenu_title, submenu_actions)

        # 创建一个 QComboBox 控件
        self.combo = QComboBox(self)
        self.combo.addItem('安全新闻')
        self.combo.addItem('https://www.secrss.com/')
        self.combo.addItem('https://www.cnvd.org.cn/')
        self.combo.addItem('https://www.yijinglab.com/news')
        self.combo.addItem('https://thehackernews.com/')
        # self.combo.addItem('')
        self.combo.currentTextChanged.connect(self.on_combobox_changed) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo, 0, 0)

        # 创建一个 QComboBox 控件
        self.combo = QComboBox(self)
        self.combo.addItem('安全工具')
        self.combo.addItem('OneForAll')
        # self.combo.addItem('')
        self.combo.currentTextChanged.connect(self.on_combobox_settxt) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo, 0, 1)

        # Nmap scan 控件
        add_label("Nmap", 1, 0)
        self.nmapip_input = add_input("localhost", 2, 0)
        self.nmaparg_input = add_input("-Pn -sS -sV -O -T3 -p22,80,443,3389", 2, 2)
        scan_button = add_button("Scan", 2, 4)
        scan_button.clicked.connect(self.run_nmap_scan)
        
        # DNS Type 控件
        add_label("DNS Type (A,AAAA,CNAME,MX...)", 3, 0)
        self.TypeDomain = add_input("unihonest.github.io", 4, 0)
        self.TypeDNS = add_input("8.8.8.8", 4, 2)
        scan_button = add_button("RUN", 4, 4)
        scan_button.clicked.connect(self.search_dns_type)

        # Whois 控件
        add_label("Whois (也许你需要根据 refer 修改 whois server.)", 5, 0)
        self.WhoisDomain = add_input("unihonest.github.io", 6, 0)
        self.WhoisDNS = add_input("whois.iana.org", 6, 2)
        scan_button = add_button("Whois", 6, 4)
        scan_button.clicked.connect(self.search_whois_info)

        # Command 控件
        add_label("Command", 7, 0)
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

    def on_combobox_settxt(self, url_string):
        if url_string == 'OneForAll':
            oneforall_txt = "子域收集工具:https://github.com/shmilylty/OneForAll\n"
            oneforall_txt1 = "查看帮助: python oneforall.py -h\n"
            oneforall_txt2 = "禁用字典测试: python oneforall.py --target domain.com --brute False run\n"
            self.result_area.setText(oneforall_txt+oneforall_txt1+oneforall_txt2)
            return

    def on_combobox_changed(self, url_string):
        if url_string == '安全新闻':
            self.result_area.setText("请选择安全新闻链接")
            return
        
        # 尝试打开选中的URL
        url = QUrl(url_string)
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open URL', f'Could not open URL: {url_string}')
            return

    def run_nmap_scan(self):
        ip = self.nmapip_input.text().strip()
        arguments = self.nmaparg_input.text().strip()
        if not ip:
            self.result_area.setText("Error: Please enter a valid IP address.")
            return
        try:
            nmap_table,logpath = NmapScan(ip, arguments)
            self.result_area.setText(nmap_table)
            self.statusBar().showMessage('Nmap logpath：' + logpath)
        except Exception as e:
            self.result_area.setText(f"Error detail: {str(e)}")
    
    def search_dns_type(self):
        TypeDomain = self.TypeDomain.text().strip()
        TypeDNS = self.TypeDNS.text().strip()
        if not TypeDomain:
            self.result_area.setText("Error: Please enter a valid Domain.")
            return
        try:
            DnsInfo,logpath2 = save_dns_records_to_log(TypeDomain, TypeDNS)
            self.result_area.setText(DnsInfo)
            self.statusBar().showMessage("DNS logpath：" + logpath2)
        except Exception as e:
            self.result_area.setText(f"Error detail: {str(e)}")

    def search_whois_info(self):
        WhoisDomain = self.WhoisDomain.text().strip()
        WhoisDNS = self.WhoisDNS.text().strip()
        if not WhoisDomain:
            self.result_area.setText("Error: Please enter a valid Domain.")
            return
        try:
            WhoisInfo,logpath3 = whois_txt(WhoisDomain, WhoisDNS)
            self.result_area.setText(WhoisInfo)
            self.statusBar().showMessage("Whois logpath：" + logpath3)
        except Exception as e:
            self.result_area.setText(f"Error detail: {str(e)}")

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

    def cancel_command(self):
        if self.process and self.process.poll() is None:          # 检查进程是否仍在运行
            self.process.terminate()                              # 发送SIGTERM信号给子进程
            self.process.wait()                                   # 等待进程结束
        self.reset_state()

    
    def reset_state(self):
        self.is_running = False
        self.execute_button.setEnabled(True)                      # 重新启用执行按钮
        self.cancel_button.setEnabled(False)                      # 禁用取消按钮
        self.statusBar().showMessage('Command run end.')

    def flush_output_buffer(self):
        with self.output_lock:
            if self.output_buffer:
                self.result_area.append("\n".join(self.output_buffer))
                self.output_buffer.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(dark_style)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())