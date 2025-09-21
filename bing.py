import json
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import time
import argparse

SHORT_LANG_MAP = {
    "cn": "zh-CN",
    "us": "en-US",
    "uk": "en-GB",
    "ca": "en-CA",
    "in": "en-IN",
    "fr": "fr-FR",
    "it": "it-IT",
    "jp": "ja-JP",
    "de": "de-DE",
}

max_workers = 8


def download_wallpapers(lang_code, short_code):
    json_url = f"https://raw.githubusercontent.com/zkeq/Bing-Wallpaper-Action/main/data/{lang_code}_all.json"
    json_file = f"{lang_code}_all.json"

    resp = requests.get(json_url)
    resp.raise_for_status()
    with open(json_file, "w", encoding="utf-8") as f:
        f.write(resp.text)

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    wallpapers = data["data"]

    folder = f"bing_wallpapers_{short_code}"
    os.makedirs(folder, exist_ok=True)
    base_url = "https://cn.bing.com"

    def download_wallpaper(wp, max_retries=3):
        urlbase = wp["urlbase"]
        startdate = wp["startdate"]
        save_path = os.path.join(folder, f"{startdate}.jpg")

        if os.path.exists(save_path):
            return None

        urls_to_try = [
            f"{base_url}{urlbase}_UHD.jpg",
            f"{base_url}{urlbase}_1920x1080.jpg",
        ]

        for attempt in range(max_retries):
            for img_url in urls_to_try:
                try:
                    r = requests.get(img_url, stream=True, timeout=15)
                    if r.status_code == 200:
                        with open(save_path, "wb") as f:
                            for chunk in r.iter_content(1024):
                                f.write(chunk)
                        if "UHD" in img_url:
                            return f"下载 UHD 成功: {save_path}"
                        else:
                            return f"下载 1920x1080 成功: {save_path}"
                except Exception as e:
                    last_error = e
            time.sleep(1)

        return f"下载失败 {startdate}: {last_error}"

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_wallpaper, wp): wp for wp in wallpapers}
        for future in tqdm(
            as_completed(futures), total=len(futures), desc=f"{short_code} 下载进度"
        ):
            result = future.result()
            if result:
                print(result)


def list_existing_languages():
    existing = []
    for folder in os.listdir("."):
        if folder.startswith("bing_wallpapers_") and os.path.isdir(folder):
            existing.append(folder.replace("bing_wallpapers_", "").lower())
    return existing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bing 壁纸下载器")
    parser.add_argument(
        "-l", "--lang", type=str, help="指定语言/地区短字符，例如 cn, us, jp"
    )
    parser.add_argument(
        "-u", "--update", action="store_true", help="查看已存在语言文件夹并更新"
    )

    args = parser.parse_args()

    if args.lang:
        short_code = args.lang.lower()
        if short_code not in SHORT_LANG_MAP:
            print(f"不支持的语言: {args.lang}")
        else:
            lang_code = SHORT_LANG_MAP[short_code]
            print(f"下载语言: {lang_code} ({short_code})")
            download_wallpapers(lang_code, short_code)

    if args.update:
        existing_langs = list_existing_languages()
        if not existing_langs:
            print("当前没有已存在的语言文件夹。")
        else:
            print("当前已存在的语言文件夹:")
            for lang in existing_langs:
                print(f"- {lang}")

            for short_code in existing_langs:
                lang_code = SHORT_LANG_MAP.get(short_code, short_code)
                print(f"更新语言: {lang_code} ({short_code})")
                download_wallpapers(lang_code, short_code)
