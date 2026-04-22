#进度保存
# -*- coding: utf-8 -*-
import json

def save_progress(words):
    with open("progress.json","w",encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False)

def load_progress():
    try:
        with open("progress.json",encoding="utf-8") as f:
            return json.load(f)
    except:
        return None