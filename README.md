# Bing 壁纸下载器

一个简单的命令行工具，用于下载 Bing 每日壁纸。

## 功能

- 下载指定语言/地区的 Bing 壁纸
- 更新已存在的壁纸文件夹

## 安装

```bash
git clone https://github.com/plsy1/bingwallpaper.git
cd bingwallpaper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## **使用说明

```bash
usage: bing.py [-h] [-l LANG] [-u]

Bing 壁纸下载器

options:
  -l LANG, --lang LANG  指定语言/地区短字符，例如 cn, us, jp
  -u, --update          查看已存在语言文件夹并更新
```

### **示例**

- 下载中国地区壁纸：

```
bing -l cn
```

- 更新壁纸：

```
bing -u
```

