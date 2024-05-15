#!/bin/bash

curl -O https://raw.githubusercontent.com/niumoo/bing-wallpaper/main/bing-wallpaper.md

mkdir -p bing_wallpapers

find bing_wallpapers -type f -size 0 -delete

while IFS='|' read -r date url; do
    date=$(echo "$date" | tr -d '[:space:]')
    url=$(echo "$url" | sed -n 's/.*(\(.*\)).*/\1/p')

    filename="${date//[^0-9-]}.jpg"
    filepath="bing_wallpapers/$filename"

    if [ -f "$filepath" ]; then
        echo "Skipping $filename as it already exists."
    else
        wget -O "$filepath" "$url" &
    fi

done < bing-wallpaper.md

wait

echo "所有图片下载完成"