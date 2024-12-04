# Python 3.12.7
__version__ = "1.0.0"
__author__ = "unihonest"

import tkinter as tk
from tkinter import messagebox, font
import math
import webbrowser
from tool.NmapCsvOut import *
from tool.WhoisGet import *
from tool.dnstypeGet import *


def NmapCommand():
    try:
        unihonestHOST = str(nmapIP.get())
        unihonestArgu = str(nmapArgu.get())

        nmlogpath = NmapCsvPrint(unihonestHOST, unihonestArgu) 

        nmapLog.delete(1.0, tk.END)                    
        nmapLog.insert(tk.END, nmlogpath) 

    except Exception as e:
        messagebox.showerror("Error", "\nError details: " + str(e))


def whoisCommand():
    try:
        unihonestdomain = str(whoisdomain.get())
        unihonestserver = str(whoisserver.get())

        whlogpath = whoisTXT(unihonestdomain,unihonestserver)

        whoisLog.delete(1.0, tk.END)      
        whoisLog.insert(tk.END, whlogpath)

    except Exception as e:
        messagebox.showerror("Input Error", "\nError details: " + str(e))


def dnstypeCommand():
    try:
        unihonestdnstypedomain = str(dnstypedomain.get())
        unihonestdnstypeserver = str(dnstypeserver.get())

        dnstypelogpath = dnstypeGet(unihonestdnstypedomain,unihonestdnstypeserver)

        dnstypeLog.delete(1.0, tk.END)      
        dnstypeLog.insert(tk.END, dnstypelogpath)

    except Exception as e:
        messagebox.showerror("Input Error", "\nError details: " + str(e))


# 定义焦点事件处理函数
def clear_default_text1(event):
    if nmapIP.get() == default_nmapIP:
        nmapIP.delete(0, tk.END)
        nmapIP.config(fg="black")


def clear_default_text2(event):
    if whoisdomain.get() == default_whoisdomain:
        whoisdomain.delete(0, tk.END)
        whoisdomain.config(fg="black")


def clear_default_text3(event):
    if dnstypedomain.get() == default_dnstypedomain:
        dnstypedomain.delete(0, tk.END)
        dnstypedomain.config(fg="black")


def open_link(url):
    # 打开指定的链接
    webbrowser.open(url)


# 设置临时窗口获取屏幕宽度和高度，计算窗口位置和大小
temp_root = tk.Tk()
temp_screen_width = temp_root.winfo_screenwidth()
temp_screen_height = temp_root.winfo_screenheight()
temp_root.destroy()

# 设置窗口大小和位置
window_width = 998
window_height = 500
x_position = math.floor((temp_screen_width - window_width) / 2)
y_position = math.floor((temp_screen_height - window_height) / 2)

# 创建主窗口
root = tk.Tk()
root.geometry(f"{window_width}x{window_height}+{int(x_position)}+{int(y_position)}")
root.title("CyberBox - unihonest")

# 设置窗口背景色为银灰色
root.configure(bg='Silver')

# 设置字体
default_font = font.Font(size=12)

# 创建一个Canvas来容纳所有组件
canvas = tk.Canvas(root, bg='Silver', width=window_width-20, height=window_height-4)
canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# 创建一个垂直滚动条
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, padx=0, pady=0, sticky='ns')

# 将Canvas的垂直滚动条与Canvas的滚动区域关联起来
canvas.config(yscrollcommand=scrollbar.set)

# 创建一个Frame来容纳其他组件
frame = tk.Frame(canvas, bg='Silver')

# 将Frame添加到Canvas中
canvas.create_window((0, 0), window=frame, anchor="nw")

# 显示功能名称
labelnmap = tk.Label(frame, text="Nmap! ", font=default_font, bg='Silver')
labelnmap.grid(row=0, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W))

# 设置输入框1
default_nmapIP = "Please enter the target IP or domain."                    # 设置默认显示信息
nmapIP = tk.Entry(frame, width=50, font=default_font, bg='Silver')          # 设定输入框宽度，字体
nmapIP.insert(0, default_nmapIP)                                            # 插入默认文本
nmapIP.grid(row=1, column=0, padx=0, pady=0)                                # 设置grid布局
nmapIP.config(fg="white")                                                   # 可以将默认文本颜色设置为灰色以区分用户输入
nmapIP.bind("<FocusIn>", clear_default_text1)                               # 绑定焦点事件

# 设置输入框2
default_text2 = "-Pn -sS -sV -O -T3 -p80,443"                               # 设置默认显示信息
nmapArgu = tk.Entry(frame, width=50, font=default_font, bg='Silver')        # 设定输入框宽度，字体
nmapArgu.insert(0, default_text2)                                           # 插入默认文本
nmapArgu.grid(row=1, column=1, padx=0, pady=0)                              # 设置grid布局

#设置功能按钮，宽度，字体
nmapButton = tk.Button(frame, width=20, font=default_font, bg='Silver', text="Start Nmap scan", command=NmapCommand)
nmapButton.grid(row=1, column=2, padx=0, pady=0, sticky=(tk.E))             # 设置grid布局

# 利用 Text 组件来展示结果，wrap='word'，文本将自动换行
nmapLog = tk.Text(frame, width=120, height=1, font=default_font, bg='Silver', wrap='word')  
nmapLog.grid(row=2, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W, tk.E, tk.S)) 
nmapLog.insert(tk.END, "Print the nmap logpath here.")

# 显示功能名称
labelwhois = tk.Label(frame, text="\nWhois! ", font=default_font, bg='Silver')
labelwhois.grid(row=3, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W))

# 设置输入框1
default_whoisdomain = "Please enter the domain."                            # 设置默认显示信息
whoisdomain = tk.Entry(frame, width=50, font=default_font, bg='Silver')     # 设定输入框宽度，字体
whoisdomain.insert(0, default_whoisdomain)                                  # 插入默认文本
whoisdomain.config(fg="white")                                              # 可以将默认文本颜色设置为灰色以区分用户输入
whoisdomain.grid(row=4, column=0)                                           # 设置grid布局
whoisdomain.bind("<FocusIn>", clear_default_text2)                          # 绑定焦点事件

# 设置输入框2
default_whoisserver = "whois.iana.org"                                     # 设置默认显示信息
whoisserver = tk.Entry(frame, width=50, font=default_font, bg='Silver')     # 设定输入框宽度，字体
whoisserver.insert(0, default_whoisserver)                                 # 插入默认文本
whoisserver.grid(row=4, column=1)                                           # 设置grid布局

# 设置功能按钮，宽度，字体
whoisbutton = tk.Button(frame, width=20, font=default_font, bg='Silver', text="Start whois", command=whoisCommand)
whoisbutton.grid(row=4, column=2, sticky=(tk.E))                            # 设置grid布局

# 利用 Text 组件来展示结果，wrap='word'，文本将自动换行
whoisLog = tk.Text(frame, width=120, height=1, font=default_font, bg='Silver', wrap='word')  
whoisLog.grid(row=5, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W, tk.E, tk.S)) 
whoisLog.insert(tk.END, "Print the whois logpath here.")

# 显示功能名称
labeldnstype = tk.Label(frame, text="\nGet-DNS-Type! ", font=default_font, bg='Silver')
labeldnstype.grid(row=6, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W))

# 设置输入框1
default_dnstypedomain = "Please enter the domain."                           # 设置默认显示信息
dnstypedomain = tk.Entry(frame, width=50, font=default_font, bg='Silver')    # 设定输入框宽度，字体
dnstypedomain.insert(0, default_dnstypedomain)                               # 插入默认文本
dnstypedomain.config(fg="white")                                             # 可以将默认文本颜色设置为灰色以区分用户输入
dnstypedomain.grid(row=7, column=0)                                          # 设置grid布局
dnstypedomain.bind("<FocusIn>", clear_default_text3)                         # 绑定焦点事件

# 设置输入框2
default_dnstypeserver2 = "8.8.8.8"                                           # 设置默认显示信息
dnstypeserver = tk.Entry(frame, width=50, font=default_font, bg='Silver')    # 设定输入框宽度，字体
dnstypeserver.insert(0, default_dnstypeserver2)                              # 插入默认文本
dnstypeserver.grid(row=7, column=1)                                          # 设置grid布局

# 设置功能按钮，宽度，字体
dnstypebutton = tk.Button(frame, width=20, font=default_font, bg='Silver', text="Start dnspython", command=dnstypeCommand)
dnstypebutton.grid(row=7, column=2, sticky=(tk.E))                           # 设置grid布局

# 利用 Text 组件来展示结果，wrap='word'，文本将自动换行
dnstypeLog = tk.Text(frame, width=120, height=1, font=default_font, bg='Silver', wrap='word')  
dnstypeLog.grid(row=8, column=0, padx=0, pady=0, columnspan=3, sticky=(tk.W, tk.E, tk.S)) 
dnstypeLog.insert(tk.END, "Print the dnstype logpath here.")

# 显示功能名称
labelsiteinfo = tk.Label(frame, text="\nSite Info! ", font=default_font, bg='Silver')
labelsiteinfo.grid(row=9, column=0, padx=0, pady=0, sticky=(tk.W))

# 定义链接和按钮文本的列表
links1 = [
    ("https://www.ip138.com/", "ip138"),
    ("https://ip.tool.chinaz.com/", "chinaz"),
    ("https://beian.miit.gov.cn/", "beian")
]

# 为每个链接创建一个按钮
for i, (url, display_text) in enumerate(links1, start=10):  
    button = tk.Button(frame, width=20, text=display_text, font=default_font, bg='Silver', command=lambda url=url: open_link(url))
    button.grid(row=i, column=0, padx=0, pady=0, sticky=(tk.W)) 

# 显示功能名称
labelcyberspace = tk.Label(frame, text="\nInternet Search Engine! ", font=default_font, bg='Silver')
labelcyberspace.grid(row=9, column=1, padx=0, pady=0, sticky=(tk.W))

links2 = [
    ("https://fofa.info/", "fofa"),
    ("https://hunter.qianxin.com/", "qianxin_hunter"),
    ("https://www.zoomeye.org/", "zoomeye")
]

# 为每个链接创建一个按钮
for i, (url, display_text) in enumerate(links2, start=10):  
    button = tk.Button(frame, width=20, text=display_text, font=default_font, bg='Silver', command=lambda url=url: open_link(url))
    button.grid(row=i, column=1, padx=0, pady=0, sticky=(tk.W)) 

# 显示功能名称
labelForeign = tk.Label(frame, text="\nForeign network! ", font=default_font, bg='Silver')
labelForeign.grid(row=9, column=2, padx=0, pady=0, sticky=(tk.W))

# 定义链接和按钮文本的列表
links3 = [
    ("https://www.google.com/", "google"),
    ("https://www.shodan.io/", "shodan"),
    ("https://github.com/", "github")
]

# 为每个链接创建一个按钮
for i, (url, display_text) in enumerate(links3, start=10):  
    button = tk.Button(frame, width=20, text=display_text, font=default_font, bg='Silver', command=lambda url=url: open_link(url))
    button.grid(row=i, column=2, padx=0, pady=0, sticky=(tk.W)) 

# 更新Canvas的scrollable区域
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# 启动主事件循环
root.mainloop()