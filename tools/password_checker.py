# -*- coding: utf-8 -*-
"""密码安全检测：强度分析 + 服务弱口令检测"""

import re
import urllib.request
from pathlib import Path

from config.settings import LOG_DIRS

# ── 内置 Top 200 常见弱口令（来源于 SecLists / RockYou 泄露统计） ──
TOP_200_WEAK = [
    "123456", "password", "12345678", "qwerty", "123456789",
    "12345", "1234", "111111", "1234567", "sunshine",
    "qwerty123", "iloveyou", "admin", "welcome", "monkey",
    "dragon", "abc123", "football", "123123", "baseball",
    "master", "666666", "qwertyuiop", "123321", "mustang",
    "1234567890", "letmein", "password1", "123", "michael",
    "654321", "superman", "1qaz2wsx", "121212", "000000",
    "qazwsx", "123qwe", "killer", "trustno1", "jordan",
    "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster",
    "soccer", "harley", "batman", "andrew", "tigger",
    "shadow", "joshua", "maggie", "bailey", "pepper",
    "robert", "cookie", "hello", "hannah", "charlie",
    "thomas", "george", "michelle", "love", "summer",
    "ashley", "nicole", "chelsea", "biteme", "matthew",
    "access", "yankees", "austin", "william", "flower",
    "555555", "princess", "dallas", "purple", "daniel",
    "starwars", "diamond", "barbara", "jessica", "anthony",
    "liverpool", "victoria", "7777777", "joseph", "alexis",
    "steven", "amanda", "grace", "qwert", "london",
    "butterfly", "charlotte", "emma", "chocolate", "ginger",
    "banana", "arsenal", "fuckyou", "elizabeth", "pokemon",
    "qwe123", "buster", "daniel", "joshua1", "1q2w3e4r",
    "marina", "jessica1", "harry", "!@#$%^&*", "654321",
    "passw0rd", "lovely", "loveme", "654321", "nathan",
    "elvis", "bubbles", "samuel", "speedy", "morgan",
    "samantha", "david", "spider", "family", "mercedes",
    "gabriel", "jasper", "millie", "spring", "sunflower",
    "november", "cheese", "robert1", "hello123", "loveyou",
    "147258", "zaq12wsx", "sweetie", "spongebob", "honey",
    "chevy", "peanut", "tucker", "blahblah", "angela",
    "ranger", "sebastian", "charles", "martin", "madison",
    "tottenham", "merlin", "extreme", "happy", "shadow1",
    "creative", "jackson", "bailey1", "ginger1", "skittles",
    "cameron", "buster1", "joshua2", "andrew1", "peanut1",
    "butterfly1", "tigger1", "sunshine1", "charlie1", "soccer1",
    "maggie1", "barbara1", "hunter1", "bailey2", "cookie1",
    "tigger2", "jessica2", "daniel1", "anthony1", "ashley1",
    "amanda1", "joseph1", "steven1", "michael1", "jordan1",
    "matthew1", "robert2", "william1", "jennifer1", "david1",
]


def _load_wordlist() -> list:
    """优先加载完整字典，否则用内置 Top 200"""
    script_dir = Path(__file__).parent.parent
    full_path = script_dir / LOG_DIRS["app"].replace("app", "") / "weak_passwords.txt"
    if full_path.exists():
        with open(full_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    return TOP_200_WEAK


SECLISTS_URL = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists/"
    "master/Passwords/Common-Credentials/10k-most-common.txt"
)

SECLISTS_GITHUB = "https://github.com/danielmiessler/SecLists"


def download_full_wordlist() -> tuple:
    """下载 SecLists Top 10000 弱口令字典，返回 (状态, 条数)"""
    script_dir = Path(__file__).parent.parent
    dir_path = script_dir / LOG_DIRS["app"].replace("app", "")
    dir_path.mkdir(parents=True, exist_ok=True)
    save_path = dir_path / "weak_passwords.txt"

    try:
        urllib.request.urlretrieve(SECLISTS_URL, save_path)
        count = 0
        with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
            count = sum(1 for _ in f)
        return (
            f"下载方式: Python urllib.request 从 GitHub Raw 直链下载\n"
            f"──────────────────────────────\n"
            f"下载地址: {SECLISTS_URL}\n"
            f"保存路径: {save_path}\n"
            f"数据来源: SecLists (Daniel Miessler)\n"
            f"GitHub:   {SECLISTS_GITHUB}\n"
            f"条数:     {count}\n"
            f"──────────────────────────────\n"
            f"下载完成！下次检测将自动使用完整字典。\n"
            f"如需删除: 删除 UserLog 目录即可"
        ), count
    except Exception as e:
        return f"下载失败: {e}", 0


# ── 密码强度分析 ──

def check_password_strength(password: str) -> str:
    """分析单个密码的强度，返回详细报告"""
    if not password:
        return "请输入密码"

    pwd = password
    wordlist = _load_wordlist()
    using = "完整字典" if len(wordlist) > 500 else "内置 Top 200"

    lines = []
    lines.append("═" * 40)
    lines.append(" 密码安全检测报告")
    lines.append("═" * 40)
    lines.append(f" 密文: {'*' * len(pwd)} ({len(pwd)} 位)")
    lines.append(f" 字典: {using} ({len(wordlist)} 条)")
    lines.append("")

    checks = []
    issues = 0

    # ① 弱口令库命中
    if pwd.lower() in wordlist:
        checks.append(("🔴", "弱口令库", f"命中常见弱口令（排名 {wordlist.index(pwd.lower())+1}）"))
        issues += 1
    else:
        checks.append(("✅", "弱口令库", "未命中"))

    # ② 长度
    if len(pwd) >= 12:
        checks.append(("✅", "长度", f"{len(pwd)} 位"))
    elif len(pwd) >= 8:
        checks.append(("🟡", "长度", f"{len(pwd)} 位（建议 ≥ 12）"))
    else:
        checks.append(("🔴", "长度", f"仅 {len(pwd)} 位（至少 8 位）"))
        issues += 1

    # ③ 字符类型
    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"\d", pwd))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", pwd))
    types = sum([has_lower, has_upper, has_digit, has_special])
    if types >= 4:
        checks.append(("✅", "字符类型", "含大小写+数字+符号"))
    elif types >= 3:
        checks.append(("🟡", "字符类型", f"含 {types} 种类型（建议 4 种）"))
    else:
        checks.append(("🔴", "字符类型", f"仅 {types} 种类型"))
        issues += 1

    # ④ 重复模式
    if re.search(r"(.)\1{2,}", pwd):
        checks.append(("🟡", "重复模式", "存在连续重复字符（如 aaa）"))
        issues += 1
    else:
        checks.append(("✅", "重复模式", "无"))

    # ⑤ 键盘序列
    keyboard_seqs = [
        "qwerty", "asdfgh", "zxcvbn", "qazwsx", "1qaz",
        "123456", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    ]
    found_seq = any(seq in pwd.lower() for seq in keyboard_seqs)
    if found_seq:
        checks.append(("🟡", "键盘序列", "存在键盘横向序列（如 qwerty）"))
        issues += 1
    else:
        checks.append(("✅", "键盘序列", "无"))

    # 综合评级
    if issues == 0:
        level = "🟢 安全"
        advice = "密码强度良好"
    elif issues <= 2:
        level = "🟡 一般"
        advice = "建议增强密码复杂度"
    else:
        level = "🔴 弱"
        advice = "强烈建议更换为 12 位以上、包含大小写+数字+符号的随机密码"

    lines.append(f" 风险等级: {level} ({issues}/5 项需改进)")
    lines.append("")
    for icon, name, detail in checks:
        lines.append(f" {icon} {name}: {detail}")
    lines.append("")
    lines.append(f" 📋 {advice}")
    lines.append("═" * 40)

    return "\n".join(lines)


def _rate_password(pwd: str, wordlist: list) -> tuple:
    """评估单个密码，返回 (issues, level_emoji, reasons)"""
    issues = 0
    reasons = []

    if pwd.lower() in wordlist:
        issues += 1
        reasons.append(f"命中弱口令库(#{wordlist.index(pwd.lower())+1})")

    if len(pwd) < 8:
        issues += 1
        reasons.append(f"长度不足({len(pwd)}位)")

    has_lower = bool(re.search(r"[a-z]", pwd))
    has_upper = bool(re.search(r"[A-Z]", pwd))
    has_digit = bool(re.search(r"\d", pwd))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", pwd))
    types = sum([has_lower, has_upper, has_digit, has_special])
    if types < 3:
        issues += 1
        reasons.append(f"字符类型少({types}种)")

    if re.search(r"(.)\1{2,}", pwd):
        issues += 1
        reasons.append("重复字符")

    keyboard_seqs = ["qwerty", "asdfgh", "zxcvbn", "qazwsx", "1qaz"]
    if any(seq in pwd.lower() for seq in keyboard_seqs):
        issues += 1
        reasons.append("键盘序列")

    if issues == 0:
        level = "🟢"
    elif issues <= 2:
        level = "🟡"
    else:
        level = "🔴"

    return issues, level, reasons


def check_password_batch(text: str) -> str:
    """批量检测多个密码（换行分割），返回汇总表格"""
    if not text or not text.strip():
        return "请至少输入一个密码"

    # 按换行分割，过滤空行
    passwords = [p.strip() for p in text.split("\n") if p.strip()]
    if not passwords:
        return "未检测到有效密码"

    wordlist = _load_wordlist()
    using = "完整字典" if len(wordlist) > 500 else "内置 Top 200"

    lines = []
    lines.append("═" * 62)
    lines.append(" 批量密码检测报告")
    lines.append("═" * 62)
    lines.append(f" 共 {len(passwords)} 个密码 | 字典: {using} ({len(wordlist)} 条)")
    lines.append("")
    lines.append(f" {'密码':<32s} {'评级':<6s} 风险说明")
    lines.append(" " + "-" * 60)

    stats = {"🟢": 0, "🟡": 0, "🔴": 0}
    for pwd in passwords:
        if len(pwd) > 30:
            display = pwd[:27] + "..."
        else:
            display = pwd
        issues, level, reasons = _rate_password(pwd, wordlist)
        stats[level] += 1
        reason_str = "; ".join(reasons) if reasons else "—"
        lines.append(f" {display:<32s} {level:<6s} {reason_str}")

    lines.append(" " + "-" * 60)
    lines.append(f" 🟢 安全: {stats['🟢']}   🟡 一般: {stats['🟡']}   🔴 弱: {stats['🔴']}")
    lines.append("═" * 62)

    return "\n".join(lines)
