# -*- coding: utf-8 -*-
"""全書設定:換一本書時,只需要改這個檔 + characters.py。

封神演義的回目是單句(「第一回 紂王女媧宮進香」),
HEADING regex 只有一個標題群組;build_wiki 會自動串接所有非空群組。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── 書 ──────────────────────────────────────────────
BOOK_TITLE = "封神演義"          # 用於 prompt 與網頁標題
N_CHAPTERS = 100                 # 全書回數(解析後檢查用)
RAW = ROOT / "data" / "fengshen_raw.txt"   # 原文純文字
EDITION_NOTE = "維基文庫本(zh-hant),全 100 回。"  # 首頁副標

# 章回標題:第(中文數字)回 單句回目
HEADING = re.compile(r"^第([一二三四五六七八九十百]+)回\s+(\S+)\s*$")

# ── 路徑 ────────────────────────────────────────────
VAULT = ROOT / "vault"
SITE = ROOT / "site"
FACTS = ROOT / "data" / "facts"

# ── LLM 端點(OpenAI 相容)──────────────────────────
API = "http://100.89.149.50:8002/v1/chat/completions"
MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"
