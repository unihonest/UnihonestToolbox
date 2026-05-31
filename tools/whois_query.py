# -*- coding: utf-8 -*-
"""原始 socket WHOIS 查询"""

import socket
from datetime import datetime
from pathlib import Path

from config.settings import LOG_DIRS, DEFAULT_WHOIS_SERVER
from utils.logger import logger


def _whois_request(domain: str, server: str, port: int = 43, timeout: int = 5) -> str:
    """通过原始 socket 连接 WHOIS 服务器查询"""
    try:
        with socket.create_connection((server, port), timeout=timeout) as sock:
            sock.sendall(f"{domain}\r\n".encode("utf-8"))
            buffer = []
            while True:
                data = sock.recv(1024)
                if not data:
                    break
                buffer.append(data)
        return "".join(data.decode("utf-8") for data in buffer)
    except socket.timeout:
        logger.error(f"连接 {server} 超时")
        return "Error: Connection timed out"
    except socket.error as e:
        logger.error(f"连接 {server} 时发生错误: {e}")
        return f"Error: {e}"


def whois_txt(domain: str, server: str = DEFAULT_WHOIS_SERVER) -> tuple:
    """查询 WHOIS 并保存日志，返回 (内容, 日志路径)"""
    if not domain or not domain.strip():
        return "Error: 请输入有效的域名或 IP", ""

    domain = domain.strip()
    server = server.strip() or DEFAULT_WHOIS_SERVER

    res = _whois_request(domain, server)

    formatted_res = (
        f"domain: {domain}\n"
        f"server: {server}\n\n"
        f"{res}"
    )

    log_folder = LOG_DIRS["whois"]
    script_dir = Path(__file__).parent.parent
    log_path = script_dir / log_folder
    log_path.mkdir(exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"whois_{current_time}.log"
    log_file_path = log_path / log_file_name

    with open(log_file_path, mode="w", encoding="utf-8") as f:
        f.write(formatted_res)

    return res, f"Logpath: {log_file_path}"
