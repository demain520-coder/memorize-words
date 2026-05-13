# -*- coding: utf-8 -*-
import json
import os

# 【新增】进度文件固定路径
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "progress.json")

# 【新增】保存当前词库路径 + 剩余单词列表
def save_progress(word_file, remaining_words):
    data = {
        "last_word_file": word_file,
        "remaining_words": remaining_words
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 【新增】读取保存的进度
def load_progress():
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# 【新增】判断是否有有效进度：有剩余单词才算有效
def has_valid_progress():
    data = load_progress()
    if not data:
        return False
    remaining = data.get("remaining_words", [])
    return len(remaining) > 0