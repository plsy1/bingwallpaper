#!/bin/bash

json_data=$(curl -s "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN")

json_url=$(echo "$json_data" | jq -r '.images[0].url')

base_url='https://cn.bing.com'
echo "JSON URL: $json_url"

new_url="${json_url/1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp/UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4}"

full_url="$base_url$new_url"
echo "Modified JSON URL: $full_url"


save_path="today-cn.jpg"

wget -O "$save_path" "$full_url"

current_directory=$(pwd)
path="$current_directory/$save_path"

echo $path

osascript -e "tell application \"System Events\" to set picture of (reference to every desktop) to \"$path\""