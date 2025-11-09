from difflib import get_close_matches
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import streamlit as st

from ai_helper import describe_yaku
from data.seed_sample import seed_yaku

st.set_page_config(page_title="麻雀役サンプル", page_icon="🀄")


def normalize(text: str) -> str:
    return text.strip().lower()


def find_yaku(query: str) -> Tuple[Optional[Dict], List[str]]:
    normalized = normalize(query)
    if not normalized:
        return None, []

    name_map = {normalize(y["name"]): y for y in seed_yaku}
    reading_map = {normalize(y["reading"]): y for y in seed_yaku}

    for key, yaku in name_map.items():
        if normalized in key:
            return yaku, []
    for key, yaku in reading_map.items():
        if normalized in key:
            return yaku, []

    candidates = list(name_map.keys()) + list(reading_map.keys())
    suggestions = get_close_matches(normalized, candidates, n=5, cutoff=0.5)
    return None, suggestions


def render_yaku(yaku: Dict) -> None:
    """役の詳細表示（AI 説明付き）。"""
    st.subheader(yaku["name"])
    st.write(f"読み: {yaku['reading']}")
    st.write(f"翻数: 門前 {yaku['han']} / 鳴き {yaku['open_han'] if yaku['open_han'] is not None else '-'}")
    st.write("AI解説:")
    with st.spinner("AI の解説を生成中..."):
        explanation, ok = describe_yaku(yaku)
    st.write(explanation)
    if not ok:
        st.warning("ローカルAIに接続できなかったため、seed の説明文を表示しています。")

    photo = yaku.get("photo")
    if photo:
        image_path = Path("assets") / photo
        if image_path.exists():
            st.image(str(image_path), caption=photo)
        else:
            st.warning(f"画像ファイルが見つかりません: {image_path}")
    else:
        st.info("この役には画像が設定されていません。")


st.title("麻雀役サンプル表示")
st.caption("テキスト入力で役を検索し、AI が解説した体で表示します。")

query = st.text_input("役名や読みを入力（例: 立直 / リーチ）")

if query:
    result, suggestions = find_yaku(query)
    if result:
        render_yaku(result)
    elif suggestions:
        st.warning("該当する役が見つかりません。もしかして: " + " / ".join(suggestions))
    else:
        st.warning("該当する役が見つかりませんでした。")
else:
    st.info("検索欄に役名を入力すると表示されます。とりあえず一例を表示します。")
    render_yaku(seed_yaku[0])
