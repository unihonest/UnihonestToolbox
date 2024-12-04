# Python 3.12.7
__version__ = "1.0.0"
__author__ = "unihonest"

import nmap
from io import StringIO
import csv
import os
from datetime import datetime
from textwrap import fill


def scan_host(unihonestHOST,unihonestArgu):
    # 创建一个nmap扫描器对象
    nmap_scanner = nmap.PortScanner() 

    # 使用提供的参数扫描主机
    nmap_scanner.scan(hosts=unihonestHOST, arguments=unihonestArgu) 

    # 检查是否有主机被扫描到
    if nmap_scanner.all_hosts():
        # 获取扫描结果的CSV格式数据
        csv_formatted_data = str(nmap_scanner.csv())
        # 获取nmap的版本信息
        nmversion = str(nmap_scanner.nmap_version())
        # 获取执行扫描时使用的命令行参数
        nmcommand = str(nmap_scanner.command_line())
        # 返回扫描结果、nmap版本和命令行参数
        return nmversion,nmcommand,csv_formatted_data
    else:
        # 如果主机不可达或不存在，打印一条消息
        print(f"Host {unihonestHOST} is not reachable or does not exist.")
        # 返回None表示扫描失败
        return None


def csv_to_items(csv_formatted_data):
    # 使用StringIO将CSV格式的字符串数据转换为文件对象
    csv_io = StringIO(csv_formatted_data.replace(';', ','))  

    # 创建一个DictReader对象，用于读取CSV数据并将其转换为字典
    # fieldnames参数指定了CSV文件中每列的名称
    reader = csv.DictReader(csv_io, fieldnames=[
        "host", "hostname", "type", "protocol", "port", "name", "state",
        "product", "extrainfo", "reason", "version", "conf", "cpe"
    ])

    # 使用列表推导式读取CSV中的所有行，并将它们存储在一个列表中，每一行都是字典
    nmlist = [row for row in reader]

    # 返回处理后列表
    return nmlist


def createLogfile(data,nmcommand,nmversion):
    # 获取当前文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__)) 

    # 设置日志文件夹名称
    nmap_folder = "nmaplog"

    # 设置日志文件夹的路径 
    nmap_path = os.path.join(script_dir, nmap_folder) 

    # 确保日志文件夹创建
    os.makedirs(nmap_path, exist_ok=True)

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

    # 设置日志文件名称
    log_file_name = f"nmap_{current_time}.csv"

    # 设置日志的路径
    log_file_path = os.path.join(nmap_path, log_file_name)

    # 提取字典的键作为CSV的表头
    fieldnames = data[0].keys()

    # 跳过列表中的第一个元素，只处理数据行
    writedata = data[1:]
    
    # 打开文件以写入CSV
    with open(log_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        # 创建DictWriter对象
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # 写入表头
        writer.writeheader()
        
        # 写入数据行
        for row in writedata:
            writer.writerow(row)

    # 写入Nmap信息
    with open(log_file_path, mode='a', encoding='utf-8') as file:
        new_content = []
        new_content.append(f",,,,,,,,,,,,")
        new_content.append(f"NmapCommand,\"{nmcommand}\",,,,,,,,,,,")
        new_content.append(f"NmapVersion,\"{nmversion}\",,,,,,,,,,,")
        for line in new_content:
            file.write(line + "\n")
    
    # 返回日志路径信息
    return (f"Logpath: {log_file_path}")


def NmapCsvPrint(unihonestHOST,unihonestArgu):
    # 传入主机信息和 nmap 参数，利用 nmap 方法获取版本、命令、扫描结果
    nmversion,nmcommand,csv_data = scan_host(unihonestHOST,unihonestArgu)
    
    # 将不好处理的 nmap csv 处理一下
    nmlist = csv_to_items(csv_data)

    # 设置日志的内容
    logpath = createLogfile(nmlist,nmcommand,nmversion)

     # 返回拼接最后的结果
    return logpath


# # 测试
# testhost = 'owaspbwa.com' #本地靶机，修改host文件测试
# testargu = '-sS -A -p443'
# NmapCsvPrint(testhost,testargu)