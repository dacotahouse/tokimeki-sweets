#!/usr/bin/env python3
"""Read-only audit of genuine Moshimo Easy Link embeds in published pages.

This script never manufactures tracking links or downloads affiliate HTML.
Only links previously issued by Moshimo are treated as affiliate codes.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import json
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = ("haeru", "cute", "gift", "wagashi", "chocolate",
              "season", "solo", "tin", "crisp")
ARTICLE = re.compile(
    r'<article\s+class="product"\s+id="(product-[^"]+)"[^>]*>(.*?)</article>',
    re.DOTALL,
)
EASYLINK = re.compile(
    r'<!--\s*START MoshimoAffiliateEasyLink\s*-->.*?'
    r'<!--\s*MoshimoAffiliateEasyLink END\s*-->',
    re.DOTALL | re.IGNORECASE,
)
CARD_ID = re.compile(r'<div\s+id="msmaflink-([^"]+)"', re.IGNORECASE)
PARAMS = re.compile(r'msmaflink\(\s*(\{.*?\})\s*\);', re.DOTALL)
NAME = re.compile(r'<h2>(.*?)</h2>', re.DOTALL)
BRAND = re.compile(r'<p class="product-brand">(.*?)</p>', re.DOTALL)
URL = re.compile(r'https://item\.rakuten\.co\.jp/[a-zA-Z0-9_./~%+-]+')

def label(html):
    return re.sub(r'<[^>]+>', '', html).strip()

def scan():
    records = []
    problems = []
    for slug in CATEGORIES:
        path = ROOT / (slug + ".html")
        if not path.exists():
            problems.append(f"{slug}.html がありません")
            continue
        content = path.read_text(encoding="utf-8")
        for product_id, article in ARTICLE.findall(content):
            name_match = NAME.search(article)
            brand_match = BRAND.search(article)
            title = label((brand_match.group(1) if brand_match else "") + " " +
                          (name_match.group(1) if name_match else product_id))
            blocks = EASYLINK.findall(article)
            direct = sorted(set(URL.findall(article.replace("\\/", "/"))))
            record = {
                "category": slug, "product_id": product_id, "name": title,
                "moshimo_cards": len(blocks),
                "rakuten_links": direct,
                "issues": [],
            }
            if not blocks:
                record["issues"].append("もしも画像付き広告コードがありません")
            for block in blocks:
                if not CARD_ID.search(block):
                    record["issues"].append("もしも広告カードのIDがありません")
                    continue
                params = PARAMS.search(block)
                if not params:
                    record["issues"].append("もしも広告データを解析できません")
                    continue
                try:
                    data = json.loads(params.group(1))
                except ValueError:
                    record["issues"].append("もしも広告データが正しいJSONではありません")
                    continue
                buttons = data.get("b_l") or []
                if not isinstance(buttons, list):
                    buttons = []
                rakuten_buttons = [
                    b for b in buttons
                    if isinstance(b, dict) and b.get("s_n") == "rakuten"
                ]
                if not rakuten_buttons:
                    record["issues"].append("楽天のもしも購入ボタンがありません")
                for b in rakuten_buttons:
                    if not isinstance(b.get("a_id"), int) or b["a_id"] <= 0:
                        record["issues"].append("もしも発行の広告IDを確認できません")
                    if urlsplit(b.get("u_url", "")).hostname != "item.rakuten.co.jp":
                        record["issues"].append("楽天ボタンのURLが不正です")
                if not data.get("p"):
                    record["issues"].append("広告カードの商品画像情報がありません")
                cid = CARD_ID.search(block).group(1)
                if data.get("eid") != cid:
                    record["issues"].append("広告カードIDと広告データIDが不一致です")
            if record["issues"]:
                problems.append(record)
            records.append(record)
    return records, problems

def main():
    records, problems = scan()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    by_page = Counter(x["category"] for x in records)
    lines = [
        "# もしもアフィリエイト・広告コード点検",
        f"実行日時: {stamp}", "",
        f"- 掲載商品: **{len(records)}件**",
        f"- 画像付きかんたんリンクあり: **{sum(x['moshimo_cards'] > 0 for x in records)}件**",
        f"- 要確認の商品: **{len(problems)}件**", "",
        "> この検査はGitHub上の既存広告コードを読み取るものです。",
        " > もしもの管理画面から広告コードを無人で発行したり、在庫を確約したりはしません。", "",
        "## 広告コード取得・確認が必要な商品",
    ]
    if not problems:
        lines.append("現時点で要確認項目はありません。")
    for x in problems:
        if isinstance(x, str):
            lines.append(f"- {x}")
        else:
            lines.append(
                f"- **{x['category']} / {x['name']}** "
                f"({x['product_id']}): {' / '.join(x['issues'])}"
            )
    lines.extend(["", "## カテゴリー別掲載数"])
    lines.extend(f"- {slug}: {by_page[slug]}件" for slug in CATEGORIES)
    Path("moshimo-audit-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path("moshimo-audit-report.json").write_text(json.dumps({
        "checked_at_utc": stamp, "products": records,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(lines))
    # Not failing a workflow when a card needs human review is intentional.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
