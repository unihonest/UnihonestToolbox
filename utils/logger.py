# -*- coding: utf-8 -*-
"""统一日志系统，替代 print"""

import logging
from pathlib import Path
from datetime import datetime

from config.settings import LOG_DIRS


def setup_logger(name: str = "UnihonestToolbox") -> logging.Logger:
    """创建带文件和控制台输出的 logger"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 控制台输出
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(ch)

    # 文件输出
    log_path = Path(__file__).parent.parent / LOG_DIRS["app"]
    log_path.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(
        log_path / f"app_{datetime.now().strftime('%Y-%m-%d')}.log",
        encoding="utf-8",
    )
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)

    return logger


logger = setup_logger()
