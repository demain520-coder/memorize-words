#学习统计
# -*- coding: utf-8 -*-
import json

def update_stats(correct):
    stats = get_stats()
    stats["total"] +=1
    if correct: stats["correct"] +=1
    with open("stats.json","w",encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False)

def get_stats():
    try:
        with open("stats.json",encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"total":0,"correct":0}