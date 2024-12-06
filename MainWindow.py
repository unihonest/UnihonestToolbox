#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QScrollArea, QVBoxLayout, QComboBox,
    QFrame, QGridLayout, QPushButton, QLabel, QLineEdit, QTextEdit,
    QMessageBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl
import sys
import subprocess
import threading
import platform
from NmapScanner import NmapScan
from DNSType import save_dns_records_to_log
from WhoisInfo import whois_txt
from DarkCSS import darkcss

# 定义 Darcula 风格的 QSS

dark_style = darkcss()

def get_system_font():
    system = platform.system().lower()
    
    if 'linux' in system:
        font_family = QFont("Hack", 6)    # kali linux字体 + 2k hidpi mod
    elif 'windows' in system:
        font_family = QFont("Consolas", 10)
    elif 'darwin' in system:  # macOS
        font_family = QFont("Menlo", 10)
    else:
        # 默认字体，如果无法识别操作系统或者是在一个不常见的操作系统上运行
        font_family = QFont("monospace", 10)
    
    return font_family


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.process = None                             # 保存子进程引用
        self.is_running = False                         # 标记命令是否正在运行

        self.setWindowTitle("工具箱 - unihonest")        # 设置窗口标题
        self.statusBar().showMessage('Status')           # 设置底部状态栏
        # 设置字体
        font = get_system_font()

        scroll_area = QScrollArea()                     # 创建可滚动区域
        self.setCentralWidget(scroll_area)              # 设置为中心部件
        scroll_area.setWidgetResizable(True)            # 允许自动调整子部件大小

        content_widget = QFrame()                       # 创建内容框架
        scroll_area.setWidget(content_widget)           # 设置滚动区域的子部件

        main_layout = QVBoxLayout()                     # 使用垂直布局作为主布局
        content_widget.setLayout(main_layout)           # 设置主布局到框架

        grid_layout = QGridLayout()                     # 创建网格布局并添加到主布局中
        main_layout.addLayout(grid_layout)

        # 定义通用组件添加函数
        def add_label(text, row, col, row_span=1, col_span=3):
            label = QLabel(text)
            grid_layout.addWidget(label, row, col, row_span, col_span)
            # 设置标签的样式表，应用线性渐变

        def add_input(placeholder, row, col, row_span=1, col_span=1):
            input_field = QLineEdit(placeholder)
            grid_layout.addWidget(input_field, row, col, row_span, col_span)
            return input_field

        def add_textarea(placeholder, row, col, row_span=1, col_span=1):
            textarea = QTextEdit(placeholder)
            grid_layout.addWidget(textarea, row, col, row_span, col_span)
            textarea.setReadOnly(True)
            textarea.setFont(font)
            return textarea

        def add_button(text, row, col, row_span=1, col_span=1):
            button = QPushButton(text)
            grid_layout.addWidget(button, row, col, row_span, col_span)
            return button

        # 创建一个 QComboBox 控件
        self.combo = QComboBox(self)
        self.combo.addItem('信息收集') 
        self.combo.addItem('https://www.ip138.com/')
        self.combo.addItem('https://ip.tool.chinaz.com/')
        self.combo.addItem('https://beian.miit.gov.cn/') # 备案
        self.combo.addItem('https://fofa.info/')
        self.combo.addItem('https://hunter.qianxin.com/')
        self.combo.addItem('https://www.zoomeye.org/')
        self.combo.addItem('https://www.google.com/')
        self.combo.addItem('https://www.shodan.io/')
        self.combo.addItem('https://github.com/')
        self.combo.currentTextChanged.connect(self.on_combobox_changed) # 当选择改变时连接到槽函数
        grid_layout.addWidget(self.combo, 0, 0)

        # Nmap scan 控件
        add_label("Nmap", 1, 0)
        self.nmapip_input = add_input("localhost", 2, 0)
        self.nmaparg_input = add_input("-Pn -sS -sV -O -T3 -p22,80,443,3389", 2, 1)
        scan_button = add_button("Scan", 2, 2)
        scan_button.clicked.connect(self.run_nmap_scan)
        
        # DNS Type 控件
        add_label("DNS Type (A,AAAA,CNAME,MX...)", 3, 0)
        self.TypeDomain = add_input("unihonest.github.io", 4, 0)
        self.TypeDNS = add_input("8.8.8.8", 4, 1)
        scan_button = add_button("RUN", 4, 2)
        scan_button.clicked.connect(self.search_dns_type)

        # Whois 控件
        add_label("Whois (Maybe you need to chang the whois server.)", 5, 0)
        self.WhoisDomain = add_input("unihonest.github.io", 6, 0)
        self.WhoisDNS = add_input("whois.iana.org", 6, 1)
        scan_button = add_button("Whois", 6, 2)
        scan_button.clicked.connect(self.search_whois_info)

        # Command 控件
        add_label("Command", 7, 0)
        self.command_input = add_input("Enter command", 8, 0)     
        self.execute_button = add_button("Exec", 8, 1)
        self.execute_button.clicked.connect(self.execute_command)
        self.cancel_button = add_button("Cancel", 8, 2)
        self.cancel_button.clicked.connect(self.cancel_command)
        self.cancel_button.setEnabled(False)                # 初始状态禁用

        # Command Executor 线程锁，缓存100ms的数据
        self.output_lock = threading.Lock()
        self.output_buffer = []
        self.output_timer = QTimer(self)
        self.output_timer.timeout.connect(self.flush_output_buffer)
        self.output_timer.start(100)                        # Refresh output buffer every 100 ms      

        # 结果输出区域
        default_txt = "Output result."
        self.result_area = add_textarea(default_txt, 9, 0, 1, 3)
        self.result_area.append("\nOther tool you can run here.")
        self.result_area.append("\npython ..\\OneForAll\\oneforall.py -h")
    
    def on_combobox_changed(self, url_string):
        if url_string == '信息收集':
            self.statusBar().showMessage('请选择一个链接打开。')
            return

        # 尝试打开选中的URL
        url = QUrl(url_string)
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open URL', f'Could not open URL: {url_string}')

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
            self.result_area.setText(f"Error during nmap scan: {str(e)}")
    
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