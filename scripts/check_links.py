#!/usr/bin/env python3
"""Read-only audit of internal links and Rakuten product URLs.

A successful HTTP response does not mean stock is available. Access blocks
(403/429) are inconclusive, not evidence that a product is discontinued.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import re

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "haeru.html", "cute.html", "gift.html",
         "wagashi.html", "chocolate.html", "season.html",
         "solo.html", "tin.html", "crisp.html", "price.html",
         "about.html", "privacy.html", "office-snacks.html"]
RAKUTEN = re.compile(r"https://item\.rakuten\.co\.jp/[A-Za-z0-9_./~%+-]+", re.I)

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for attr in ("href", "src"):
            if a.get(attr):
                self.refs.append(a[attr])

def inspect_site():
    parsers = {}
    errors = []
    product_urls = set()
    for name in PAGES:
        file = ROOT / name
        if not file.is_file():
            errors.append(f"{name}: ファイルが見つかりません")
            continue
        content = file.read_text(encoding="utf-8")
        parser = PageParser()
        parser.feed(content)
        parsers[name] = parser
        product_urls.update(x.rstrip(".,;") for x in RAKUTEN.findall(content.replace("\\/", "/")))
    for name, parser in parsers.items():
        for ref in parser.refs:
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or ref.startswith(("//", "#")) and not ref.startswith("#"):
                continue
            target = unquote(parsed.path) or name
            if not target or target.startswith("/"):
                continue
            path = (ROOT / target).resolve()
            if not path.is_relative_to(ROOT.resolve()):
                errors.append(f"{name}: 対象外のパス {ref}")
            elif not path.exists():
                errors.append(f"{name}: リンク先がありません {ref}")
            elif parsed.fragment and path.name in parsers:
                if unquote(parsed.fragment) not in parsers[path.name].ids:
                    errors.append(f"{name}: アンカーがありません {ref}")
    return errors, sorted(product_urls)

def check_url(url):
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"})
    try:
        with urlopen(request, timeout=12) as response:
            status = response.status
    except HTTPError as exc:
        status = exc.code
    except (URLError, TimeoutError, OSError) as exc:
        return {"url": url, "status": "不明", "note": type(exc).__name__}
    if status in (404, 410):
        note = "404/410：販売ページの再確認が必要"
    elif status in (403, 429):
        note = "アクセス制限の可能性・判定不可"
    elif status < 400:
        note = "ページ応答あり・在庫は未確認"
    else:
        note = "HTTP応答を要確認"
    return {"url": url, "status": status, "note": note}

def main():
    errors, urls = inspect_site()
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        jobs = [pool.submit(check_url, url) for url in urls]
        for job in as_completed(jobs):
            results.append(job.result())
    results.sort(key=lambda x: x["url"])
    noteworthy = [x for x in results if x["status"] == "不明" or x["status"] >= 400]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# ときめきスイーツ図鑑・リンク確認",
        f"実行日時: {stamp}", "",
        f"- 内部リンクの問題: {len(errors)}件",
        f"- 楽天の商品URL: {len(urls)}件",
        f"- 外部応答で要確認・判定不可: {len(noteworthy)}件", "",
        "**ご注意:** HTTP応答だけで在庫・取り扱い終了を判定しません。"
        "商品の変更や削除は、同一規格と販売状況を人が確かめてから行います。", "",
        "## 内部リンク",
        *( [f"- {e}" for e in errors] if errors else ["問題は見つかりませんでした。"] ),
        "", "## 楽天の要確認URL",
        *( [f"- {r['status']} {r['url']} — {r['note']}" for r in noteworthy] if noteworthy else ["該当なし"] ),
    ]
    Path("link-check-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    Path("link-check-report.json").write_text(json.dumps({
        "checked_at_utc": stamp, "internal_errors": errors,
        "rakuten_urls": urls, "responses": results
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(lines[:9]))
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
