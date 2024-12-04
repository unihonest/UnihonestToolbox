# Python 3.12.7
__version__ = "1.0.0"
__author__ = "unihonest"

import socket
import os
from datetime import datetime


# https://developer.aliyun.com/article/1193027
def whois_request(domain: str, server: str, port=43, timeout=5) -> str:
    # 创建连接
    sock = socket.create_connection((server, port))
    sock.settimeout(timeout)

    # 发送请求
    sock.send(("%s\r\n" % domain).encode("utf-8"))

    # 接收数据
    buff = bytes()
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        buff += data

    # 关闭链接
    sock.close()

    # 返回缓存的http信息
    return buff.decode("utf-8")


def createLog(res):
    # 获取当前文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__)) 

    # 设置日志文件夹名称
    nmap_folder = "whoislog"

    # 设置日志文件夹的路径 
    nmap_path = os.path.join(script_dir, nmap_folder) 

    # 确保日志文件夹创建
    os.makedirs(nmap_path, exist_ok=True)

    # 获取当前时间
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 

    # 设置日志文件名称
    log_file_name = f"whois_{current_time}.log"

    # 设置日志的路径
    log_file_path = os.path.join(nmap_path, log_file_name)

    # 保存成日志文件
    with open(log_file_path, mode='w', encoding='utf-8') as file:
        file.write(res)

    # 返回日志路径信息
    return (f"Logpath: {log_file_path}")

def whoisTXT(unihonestdomain,unihonestserver):
    # 查询域名信息
    res = whois_request(unihonestdomain, unihonestserver)

    res1 = "domain: " + unihonestdomain + "\nserver: " + unihonestserver + "\n\n" + res

    # 记录日志
    logpath = createLog(res1)

    # 返回whois信息
    return logpath