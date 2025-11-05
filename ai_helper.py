"""Ollama を使って役の説明を生成するヘルパー."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Dict, Tuple

DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
DEFAULT_ENDPOINT = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")


def _build_prompt(yaku: Dict[str, str]) -> str:
    base = yaku.get("description", "")
    name = yaku.get("name", "この役")
    reading = yaku.get("reading", "")
    han = yaku.get("han", "-")
    open_han = yaku.get("open_han", "-")
    menzen_only = yaku.get("menzen_only") or "鳴き可"

    return (
        "あなたは麻雀役を初心者に教えるプロ講師です。以下の情報だけを材料にして、"
        "事実に忠実で簡潔な解説を日本語で作成してください。未知の情報を推測したり、"
        "ドラや配点など seed に書かれていない要素を勝手に語らないでください。\n"
        "出力フォーマットは必ず次のとおりにします:\n"
        "【概要】1文で要点\n"
        "【ポイント】\n"
        "- 箇条書き1\n"
        "- 箇条書き2\n"
        "【初心者向けアドバイス】1文\n"
        "----------\n"
        f"役名: {name}\n"
        f"読み: {reading}\n"
        f"門前翻: {han}\n"
        f"鳴き翻: {open_han if open_han is not None else '非対応'}\n"
        f"分類: {menzen_only}\n"
        f"seed説明: {base}\n"
    )


def _post_to_ollama(prompt: str) -> str:
    payload = json.dumps(
        {
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9,
                "repeat_penalty": 1.1,
                "num_predict": 512,
            },
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{DEFAULT_ENDPOINT}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("response", "").strip()


def describe_yaku(yaku: Dict[str, str]) -> Tuple[str, bool]:
    """役の情報を元に Ollama へ問い合わせ、説明文と成功フラグを返す。"""
    prompt = _build_prompt(yaku)

    try:
        response_text = _post_to_ollama(prompt)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
        response_text = ""

    if response_text:
        return response_text, True

    base = yaku.get("description", "説明文を取得できませんでした。")
    fallback = (
        f"{yaku.get('name', 'この役')}（{yaku.get('reading', '')}）の説明生成に失敗しました。\n"
        f"代わりに seed の説明を表示します。\n{base}"
    )
    return fallback, False
