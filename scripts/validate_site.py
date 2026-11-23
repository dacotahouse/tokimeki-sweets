#!/usr/bin/env python3
"""Validate the nine-category *published HTML* without rebuilding it.

The legacy build_site.py is not currently a faithful source for the live site.
This validator reads existing pages only; it never writes or regenerates them.
"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
CATEGORIES = ("haeru", "cute", "gift", "wagashi", "chocolate",
              "season", "solo", "tin", "crisp")

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.product_ids = []
        self.category_links = []
        self.affiliate_ids = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        element_id = attr.get("id", "")
        if element_id.startswith("product-"):
            self.product_ids.append(element_id)
        if element_id.startswith("msmaflink-"):
            self.affiliate_ids.append(element_id)
        if tag == "a" and attr.get("href", "").split("#", 1)[0] in {
            s + ".html" for s in CATEGORIES
        }:
            self.category_links.append(attr["href"].split("#", 1)[0])

def parse(path):
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page

def main():
    problems = []
    home = ROOT / "index.html"
    if not home.exists():
        problems.append("index.html がありません")
    else:
        page = parse(home)
        missing = {s + ".html" for s in CATEGORIES} - set(page.category_links)
        if missing:
            problems.append(f"トップページにカテゴリー導線がありません: {sorted(missing)}")

    product_to_pages = {}
    for slug in CATEGORIES:
        path = ROOT / f"{slug}.html"
        if not path.exists():
            problems.append(f"{slug}.html がありません")
            continue
        page = parse(path)
        if len(page.product_ids) != 10:
            problems.append(f"{slug}.html: 商品カード {len(page.product_ids)}件（期待10件）")
        for x, count in Counter(page.product_ids).items():
            if count != 1:
                problems.append(f"{slug}.html: 商品IDが重複 {x}")
            product_to_pages.setdefault(x, []).append(slug)
        for x, count in Counter(page.affiliate_ids).items():
            if count != 1:
                problems.append(f"{slug}.html: 広告カードIDが重複 {x}")
    for product_id, pages in product_to_pages.items():
        if len(pages) > 1:
            problems.append(f"{product_id}: 複数カテゴリーに掲載 {', '.join(pages)}")

    print("9カテゴリーと各10商品の公開HTML整合性チェック")
    if problems:
        for issue in problems:
            print("ERROR:", issue)
        return 1
    print(f"PASS: {len(CATEGORIES)}カテゴリー、{len(product_to_pages)}商品")
    return 0

if __name__ == "__main__":
    sys.exit(main())
