#!/bin/bash



json_data=$(curl -s "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN")

json_url=$(echo "$json_data" | jq -r '.images[0].url')

base_url='https://bing.com'
echo "JSON URL: $json_url"

new_url="${json_url/1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp/UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4}"

full_url="$base_url$new_url"
echo "Modified JSON URL: $full_url"

current_date=$(date +'%Y-%m-%d')
current_directory=$(pwd)
save_path="$current_directory/bing_wallpapers_cn/$current_date.jpg"

wget -O "$save_path" "$full_url"

echo $save_path

osascript -e "tell application \"System Events\" to set picture of (reference to every desktop) to \"$save_path\""