from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data.seed_sample import seed_yaku

ASSETS_DIR = Path("assets")


def main() -> None:
    missing = []
    total = 0

    for yaku in seed_yaku:
        photo = yaku.get("photo")
        if not photo:
            continue  
        total += 1
        img_path = ASSETS_DIR / photo
        if not img_path.exists():
            missing.append(str(img_path))

    print(f"画像設定がある役: {total} 件")
    if missing:
        print("見つからないファイル:")
        for path in missing:
            print(f" - {path}")
    else:
        print("すべての画像ファイルが assets/ に存在します。")


if __name__ == "__main__":
    main()
