#错题本
# word/wrong_book.py
import json
import os

# 使用基于当前文件位置的绝对路径
WRONG_FILE = os.path.join(os.path.dirname(__file__), "wrong_words.json")

def load_wrong_words():
    """加载错题本"""
    if not os.path.exists(WRONG_FILE):
        return []
    try:
        with open(WRONG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_wrong_words(words):
    """保存错题本"""
    with open(WRONG_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

def add_wrong_word(word, meaning):
    """添加单词到错题本（去重）"""
    wrong = load_wrong_words()
    for w in wrong:
        if w[0] == word:
            return
    wrong.append([word, meaning])
    save_wrong_words(wrong)

def clear_wrong_words():
    """清空错题本"""
    if os.path.exists(WRONG_FILE):
        os.remove(WRONG_FILE)