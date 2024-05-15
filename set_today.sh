#!/bin/bash

current_directory=$(pwd)
current_date=$(date +"%Y-%m-%d")
path="$current_directory/bing_wallpapers/$current_date.jpg"

echo $path

osascript -e "tell application \"System Events\" to set picture of (reference to every desktop) to \"$path\""