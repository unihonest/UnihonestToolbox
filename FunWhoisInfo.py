#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "unihonest"
__license__ = "GNU General Public License v3.0"

import socket
from datetime import datetime
from pathlib import Path
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def whois_request(domain: str, server: str, port=43, timeout=5) -> str:
    try:
        with socket.create_connection((server, port), timeout=timeout) as sock:
            sock.sendall(f"{domain}\r\n".encode("utf-8"))

            # 接收数据
            buffer = []
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                buffer.append(data)

        # 将所有接收的数据拼接成一个字符串
        response = ''.join(data.decode("utf-8") for data in buffer)
        return response

    except socket.timeout:
        logging.error(f"连接 {server} 超时")
        return "Error: Connection timed out"
    except socket.error as e:
        logging.error(f"连接 {server} 时发生错误: {e}")
        return f"Error: {e}"

def create_log_directory(log_folder: str) -> Path:
    """创建日志文件夹并返回其路径"""
    script_dir = Path(__file__).parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)
    return log_path

def save_to_log(log_path: Path, content: str) -> str:
    """将内容保存到日志文件并返回日志路径"""
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"whois_{current_time}.log"
    log_file_path = log_path / log_file_name

    with open(log_file_path, mode='w', encoding='utf-8') as file:
        file.write(content)

    return f"Logpath: {log_file_path}"

def whois_txt(unihonest_domain: str, unihonest_server: str) -> str:
    """查询域名的 WHOIS 信息并保存到日志文件"""
    # 查询域名信息
    res = whois_request(unihonest_domain, unihonest_server)

    # 格式化输出
    formatted_res = (
        f"domain: {unihonest_domain}\n"
        f"server: {unihonest_server}\n\n"
        f"{res}"
    )

    # 创建日志文件夹
    log_path = create_log_directory("whoislog")

    # 保存日志
    logpath = save_to_log(log_path, formatted_res)

    # 返回日志路径信息
    return res,logpath

