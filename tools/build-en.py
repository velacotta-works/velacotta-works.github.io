#!/usr/bin/env python3
"""index.html から英語版 en/index.html を生成する。

日本語版（index.html）が原本。本文の日英切り替えはページ内のJS辞書が行うため、
このスクリプトが書き換えるのは「JSでは切り替えられない部分」＝ <head> のメタ情報だけ。
リンクをSlack/LinkedIn等に貼ったときのプレビューカードを英語にするために必要。

使い方（リポジトリのルートで実行）:
    python3 tools/build-en.py

index.html を編集したら毎回これを実行して en/index.html を作り直すこと。
置換に失敗した場合はエラーで止まる（HTML側の変更に気づかず古い英語版が残るのを防ぐため）。
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
DST = ROOT / "en" / "index.html"

BASE = "https://velacotta-works.github.io/"
EN_URL = BASE + "en/"

TITLE_EN = "Miho | Workflow Automation &amp; Ops Support (Notion / GAS / AI) | VelaCotta Works"
DESC_EN = (
    "Workflow automation with Notion, GAS and AI, sales and admin support, MEO and course "
    "content. I find where work gets stuck, turn it into a system, and build it until it runs. "
    "Get in touch about working together."
)
OG_DESC_EN = (
    "I find where work gets stuck, turn it into a system, and build it until it runs. "
    "Workflow automation with Notion, GAS and AI, sales and admin support, MEO and course content."
)
TW_TITLE_EN = "Miho | Workflow Automation &amp; Ops Support | VelaCotta Works"
OG_ALT_EN = (
    "VelaCotta Works / Miho - Finding where work gets stuck, turning it into a system, "
    "and building it until it runs."
)

# (説明, 置換前, 置換後)。置換前が本文にちょうど1回現れることを確認してから置き換える。
REPLACEMENTS = [
    (
        "html要素のlang属性",
        '<html lang="ja">',
        '<html lang="en">',
    ),
    (
        "ページタイトル",
        "<title>Miho ｜ 業務効率化・自動化サポート（Notion / GAS / AI）｜VelaCotta Works</title>",
        f"<title>{TITLE_EN}</title>",
    ),
    (
        "description",
        '<meta name="description" content="現場業務の仕組み化・自動化（Notion / GAS / AI）、営業・事務サポート、MEO・教材制作。業務の詰まりを見つけ、仕組みにして、動くところまで作ります。お仕事のご相談はこちらから。">',
        f'<meta name="description" content="{DESC_EN}">',
    ),
    (
        "og:url",
        f'<meta property="og:url" content="{BASE}">',
        f'<meta property="og:url" content="{EN_URL}">',
    ),
    (
        "og:locale",
        '<meta property="og:locale" content="ja_JP">',
        '<meta property="og:locale" content="en_US">',
    ),
    (
        "og:title",
        '<meta property="og:title" content="Miho ｜ 業務効率化・自動化サポート（Notion / GAS / AI）｜VelaCotta Works">',
        f'<meta property="og:title" content="{TITLE_EN}">',
    ),
    (
        "og:description",
        '<meta property="og:description" content="業務の詰まりを見つけ、仕組みにして、動くところまで。Notion・GAS・AIでの業務効率化、営業・事務サポート、MEO・教材制作の制作実績。">',
        f'<meta property="og:description" content="{OG_DESC_EN}">',
    ),
    (
        "og:image:alt",
        '<meta property="og:image:alt" content="VelaCotta Works / Miho — 業務の詰まりを見つけ、仕組みにして、動くところまで。">',
        f'<meta property="og:image:alt" content="{OG_ALT_EN}">',
    ),
    (
        "twitter:title",
        '<meta name="twitter:title" content="Miho ｜ 業務効率化・自動化サポート｜VelaCotta Works">',
        f'<meta name="twitter:title" content="{TW_TITLE_EN}">',
    ),
    (
        "twitter:description",
        '<meta name="twitter:description" content="業務の詰まりを見つけ、仕組みにして、動くところまで。Notion・GAS・AI・MEO・教材制作の制作実績。">',
        f'<meta name="twitter:description" content="{OG_DESC_EN}">',
    ),
    (
        "canonical",
        f'<link rel="canonical" href="{BASE}">',
        f'<link rel="canonical" href="{EN_URL}">',
    ),
]


def main() -> int:
    if not SRC.exists():
        print(f"エラー: {SRC} が見つかりません。リポジトリのルートで実行してください。")
        return 1

    html = SRC.read_text(encoding="utf-8")
    errors = []

    for label, before, after in REPLACEMENTS:
        count = html.count(before)
        if count != 1:
            errors.append(f"  - {label}: 想定した記述が {count} 件見つかりました（1件であるべき）")
            continue
        html = html.replace(before, after, 1)

    if errors:
        print("エラー: index.html の記述が変わったため英語版を生成できません。")
        print("\n".join(errors))
        print("\ntools/build-en.py の REPLACEMENTS を実際のindex.htmlに合わせて直してください。")
        return 1

    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(html, encoding="utf-8")
    print(f"生成しました: {DST.relative_to(ROOT)}（{len(html.encode('utf-8')) // 1024} KB）")
    print(f"日本語: {BASE}")
    print(f"英語  : {EN_URL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
