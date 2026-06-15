# -*- coding: utf-8 -*-
"""用户设置管理器：读取/写入用户自定义配置（持久化到 JSON）"""

import json
from pathlib import Path

from config.settings import HTTP_PROXY as DEFAULT_PROXY


# 用户配置文件路径
SETTINGS_FILE = Path(__file__).parent.parent / "config" / "user_settings.json"

# 默认值
DEFAULTS = {
    "proxy": DEFAULT_PROXY,
    "proxy_enabled": True,
}


def _load() -> dict:
    """从 JSON 文件读取用户设置，不存在则返回默认"""
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {**DEFAULTS, **data}
        except (json.JSONDecodeError, ValueError):
            pass
    return DEFAULTS.copy()


def _save(data: dict) -> None:
    """写入用户设置到 JSON 文件"""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_proxy() -> str:
    """获取当前代理地址"""
    return _load()["proxy"]


def set_proxy(value: str) -> None:
    """更新代理地址并持久化"""
    data = _load()
    data["proxy"] = value
    _save(data)


def is_proxy_enabled() -> bool:
    """代理是否启用"""
    return _load()["proxy_enabled"]


def set_proxy_enabled(enabled: bool) -> None:
    """启用/禁用代理并持久化"""
    data = _load()
    data["proxy_enabled"] = enabled
    _save(data)
