# -*- coding: utf-8 -*-
"""維基文庫 → data/fengshen_raw.txt
逐卷抓 zh.wikisource.org 的《封神演義》(zh-hant 轉換),輸出格式與 epub_to_txt 相同:
回目標題獨立一行、每段一行且以全形空格開頭。
頁面快取在 data/wikisource_cache/,可中斷重跑。
"""
import html as html_mod
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import BOOK_TITLE, N_CHAPTERS, RAW, ROOT

CACHE = ROOT / "data" / "wikisource_cache"
BASE = "https://zh.wikisource.org/zh-hant/"
UA = {"User-Agent": "fengshen-wiki/1.0 (personal classical-novel wiki builder)"}

# 目前回的標題在 header 表格內,回數與回目之間是「空格」;
# 上/下回導覽連結中間隔的是 <br />,不會誤中
TITLE_RE = re.compile(r"(第[一二三四五六七八九十百]+回) +([^<\s]+)")
P_RE = re.compile(r"<p>(.*?)</p>", re.S)


def fetch(chap: int) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"ch_{chap:03d}.html"
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    url = BASE + urllib.parse.quote(f"{BOOK_TITLE}/卷{chap:03d}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        page = r.read().decode("utf-8")
    cached.write_text(page, encoding="utf-8")
    time.sleep(0.5)  # 對維基文庫客氣一點
    return page


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", "", html_mod.unescape(s))


def parse(page: str, chap: int):
    """回傳 (標題行, [段落, ...])"""
    body = page[page.find("mw-parser-output"):]
    end = body.find("printfooter")
    if end > 0:
        body = body[:end]
    m = TITLE_RE.search(body)
    if not m:
        raise ValueError(f"卷{chap}: 找不到回目標題")
    heading = f"{m.group(1)} {m.group(2)}"
    paras = [t for t in (strip_tags(p) for p in P_RE.findall(body)) if t]
    if sum(len(p) for p in paras) < 1000:
        raise ValueError(f"卷{chap}: 正文太短,疑似解析失敗")
    return heading, paras


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console 預設 cp950
    out = []
    for chap in range(1, N_CHAPTERS + 1):
        heading, paras = parse(fetch(chap), chap)
        out.append(heading)
        out.extend("　" + p for p in paras)
        out.append("")
        print(f"{heading}  ({len(paras)} 段, {sum(len(p) for p in paras)} 字)", flush=True)
    RAW.parent.mkdir(exist_ok=True)
    RAW.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"written {RAW}")


if __name__ == "__main__":
    main()
