# -*- coding: utf-8 -*-
# GREat@背单词修复
import tkinter as tk
from tkinter import font, messagebox
import random
import sys
import os

class WordApp:
    def __init__(self, root, word_file):
        self.root = root
        self.root.title("GREat@背单词")
        self.root.geometry("760x860")  
        self.root.resizable(False, False)

        # 加载单词列表
        self.words = self.load_words(word_file)
        self.total = len(self.words)
        self.current = None

        # 字体设置
        self.word_font = font.Font(size=36, weight="bold")
        self.meaning_font = font.Font(size=22)
        self.btn_font = font.Font(size=22)
        self.stat_font = font.Font(size=24, weight="bold")

        # ---------------------- 顶部状态栏（绿色） ----------------------
        self.status_frame = tk.Frame(root, bg="#009E5F", height=100)
        self.status_frame.pack(fill=tk.X, anchor=tk.N)
        self.status_label = tk.Label(
            self.status_frame, text=f"(剩余:{len(self.words)})",
            bg="#009E5F", fg="yellow", font=self.stat_font
        )
        self.status_label.pack(pady=30)

        # ---------------------- 单词 + 释义区域 ----------------------
        self.word_frame = tk.Frame(root, bg="white", height=250)
        self.word_frame.pack(fill=tk.X, pady=20)

        self.word_label = tk.Label(self.word_frame, text="", bg="white", font=self.word_font)
        self.word_label.pack(pady=15)

        # 分割线
        self.line = tk.Frame(self.word_frame, bg="#CCCCCC", height=2)
        self.line.pack(fill=tk.X, padx=100)

        self.meaning_label = tk.Label(self.word_frame, text="", bg="white", font=self.meaning_font)
        self.meaning_label.pack(pady=20)

        # ---------------------- 按钮区域 ----------------------
        self.btn_frame = tk.Frame(root, bg="#F0F0F0")
        self.btn_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 我忘了
        self.btn1 = tk.Button(
            self.btn_frame, text="我忘了", font=self.btn_font,
            bg="#FFFFFF", relief=tk.FLAT, command=self.forget
        )
        self.btn1.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        # 我记得
        self.btn2 = tk.Button(
            self.btn_frame, text="我记得", font=self.btn_font,
            bg="#FFFFFF", relief=tk.FLAT, command=self.remember
        )
        self.btn2.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.grid_rowconfigure(0, weight=1)

        # ---------------------- Settings 按钮 ----------------------
        self.set_btn = tk.Button(
            root, text="Settings", font=font.Font(size=18),
            relief=tk.FLAT, bg="#E0E0E0", command=self.show_settings
        )
        self.set_btn.pack(fill=tk.X, padx=20, pady=15)

        # 键盘快捷键（a / s / ← / →）
        root.bind("<a>", lambda e: self.forget())
        root.bind("<s>", lambda e: self.remember())
        root.bind("<Left>", lambda e: self.forget())
        root.bind("<Right>", lambda e: self.remember())

        # 开始显示第一个单词
        self.next_word()

    def load_words(self, filepath):
        """读取单词文件"""
        words = []
        if not os.path.exists(filepath):
            messagebox.showerror("错误", f"文件不存在：{filepath}")
            sys.exit(1)

        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "\t" in line:
                    w, m = line.split("\t", 1)
                else:
                    arr = line.split(" ", 1)
                    if len(arr) < 2:
                        continue
                    w, m = arr
                words.append((w.strip(), m.strip()))

        random.shuffle(words)
        return words

    def next_word(self):
        if not self.words:
            self.word_label.config(text="🎉 背完啦！")
            self.meaning_label.config(text="恭喜完成学习")
            self.status_label.config(text="(剩余:0)")
            self.btn1.config(state=tk.DISABLED)
            self.btn2.config(state=tk.DISABLED)
            return

        self.current = self.words.pop()
        w, m = self.current
        self.word_label.config(text=w)
        self.meaning_label.config(text=m)
        self.status_label.config(text=f"(剩余:{len(self.words)})")

    def forget(self):
        """忘了：放回队列末尾"""
        self.words.insert(0, self.current)
        self.next_word()

    def remember(self):
        """记得：直接下一个"""
        self.next_word()

    def show_settings(self):
        messagebox.showinfo("设置", "快捷键：A / S / ← / →\n退出直接关闭窗口")

if __name__ == "__main__":
    # 读取 08red/11.txt
    file_path = r"E:\git\memorize-words\08red\11.txt"

    # 如果需要测试，把上面注释，打开下面这行
    # file_path = "test.txt"

    window = tk.Tk()
    app = WordApp(window, file_path)
    window.mainloop()