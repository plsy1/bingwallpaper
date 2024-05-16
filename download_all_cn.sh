#!/bin/zsh


cd /Users/y1/Pictures/wallpaper/bingwallpaper

curl -O https://raw.githubusercontent.com/niumoo/bing-wallpaper/main/zh-cn/bing-wallpaper.md

mkdir -p bing_wallpapers_cn

find bing_wallpapers_cn -type f -size 0 -delete

while read -r line; do
    date=$(echo "$line" | cut -d '|' -f 1 | tr -d ' ')
    filename="${date//[^0-9-]}.jpg"
    filepath="bing_wallpapers_cn/$filename"
    if [ -f "$filepath" ]; then
        echo "Skipping $filename as it already exists."
    else
        url=$(echo "$line" | grep -oP '(?<=\()([^)]+)(?=\))' | tail -n1)
        wget -O "$filepath" "$url" &
    fi
done < bing-wallpaper.md

wait

echo "所有图片下载完成"
