# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
import random
import sys
import os

class GREApp:
    def __init__(self, master, word_file):
        self.master = master
        self.master.title("GREat@背单词")
        self.master.geometry("800x600")
        self.master.resizable(False, False)

        # 加载单词
        self.words = self.load_words(word_file)
        self.total_words = len(self.words)
        self.remaining = self.total_words
        self.current_word = None
        self.current_meaning = None

        # 字体设置
        self.title_font = font.Font(size=24, weight="bold")
        self.word_font = font.Font(size=36, weight="bold")
        self.meaning_font = font.Font(size=20)
        self.btn_font = font.Font(size=20)
        self.status_font = font.Font(size=18, weight="bold")

        # 状态栏（剩余单词数）
        self.status_bar = tk.Frame(master, bg="green", height=80)
        self.status_bar.pack(fill=tk.X, anchor=tk.N)
        self.status_label = tk.Label(
            self.status_bar,
            text=f"(剩余:{self.remaining})",
            bg="green",
            fg="yellow",
            font=self.status_font
        )
        self.status_label.pack(pady=20)

        # 单词显示区
        self.word_frame = tk.Frame(master, bg="white", height=150)
        self.word_frame.pack(fill=tk.X)
        self.word_label = tk.Label(
            self.word_frame,
            text="",
            bg="white",
            font=self.word_font
        )
        self.word_label.pack(pady=20)
        self.separator = tk.Frame(self.word_frame, bg="gray", height=2)
        self.separator.pack(fill=tk.X, padx=20)
        self.meaning_label = tk.Label(
            self.word_frame,
            text="",
            bg="white",
            font=self.meaning_font
        )
        self.meaning_label.pack(pady=10)

        # 按钮区
        self.btn_frame = tk.Frame(master, bg="green")
        self.btn_frame.pack(fill=tk.BOTH, expand=True)
        # 配置网格布局，让两个按钮平分空间
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        self.btn_frame.grid_rowconfigure(0, weight=1)

        # 我忘了按钮
        self.forget_btn = tk.Button(
            self.btn_frame,
            text="我忘了",
            font=self.btn_font,
            bg="#f0f0f0",
            command=self.on_forget
        )
        self.forget_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 我记得按钮
        self.remember_btn = tk.Button(
            self.btn_frame,
            text="我记得",
            font=self.btn_font,
            bg="#f0f0f0",
            command=self.on_remember
        )
        self.remember_btn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 设置按钮（修复原拼写错误 Setttings → Settings）
        self.settings_btn = tk.Button(
            master,
            text="Settings",
            font=self.btn_font,
            command=self.on_settings
        )
        self.settings_btn.pack(fill=tk.X, padx=10, pady=10)

        # 绑定键盘事件
        self.master.bind("<a>", lambda e: self.on_forget())
        self.master.bind("<s>", lambda e: self.on_remember())
        self.master.bind("<Left>", lambda e: self.on_forget())
        self.master.bind("<Right>", lambda e: self.on_remember())

        # 初始化第一个单词
        self.next_word()

    def load_words(self, file_path):
        """加载单词文件，格式：单词\t释义（支持utf-8编码）"""
        words = []
        if not os.path.exists(file_path):
            print(f"错误：文件 {file_path} 不存在！")
            sys.exit(1)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # 按制表符分割，兼容空格分割的情况
                    if "\t" in line:
                        word, meaning = line.split("\t", 1)
                    else:
                        parts = line.split(maxsplit=1)
                        if len(parts) < 2:
                            continue
                        word, meaning = parts
                    words.append( (word.strip(), meaning.strip()) )
            random.shuffle(words)
            return words
        except Exception as e:
            print(f"加载单词文件失败：{str(e)}")
            sys.exit(1)

    def next_word(self):
        """加载下一个单词"""
        if not self.words:
            self.word_label.config(text="背完啦！🎉")
            self.meaning_label.config(text="恭喜完成本次背诵！")
            self.status_label.config(text="(剩余:0)")
            self.forget_btn.config(state=tk.DISABLED)
            self.remember_btn.config(state=tk.DISABLED)
            return
        self.current_word, self.current_meaning = self.words.pop()
        self.word_label.config(text=self.current_word)
        self.meaning_label.config(text=self.current_meaning)
        self.remaining = len(self.words)
        self.status_label.config(text=f"(剩余:{self.remaining})")

    def on_forget(self):
        """我忘了：单词放回列表末尾，下次再背"""
        self.words.insert(0, (self.current_word, self.current_meaning))
        self.next_word()

    def on_remember(self):
        """我记得：单词移除，不再显示"""
        self.next_word()

    def on_settings(self):
        """设置按钮：简单弹窗提示"""
        tk.messagebox.showinfo("设置", "当前版本仅支持基础背诵功能，更多功能敬请期待！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 bei.py [单词文件路径]")
        print("示例: python3 bei.py 08red/11.txt")
        sys.exit(1)
    word_file = sys.argv[1]
    root = tk.Tk()
    app = GREApp(root, word_file)
    root.mainloop()