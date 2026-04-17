#ui界面
# ui/window.py
import tkinter as tk
from tkinter import font, messagebox, scrolledtext
from word.wrong_book import add_wrong_word, load_wrong_words, clear_wrong_words
import os

class WordApp:
    def __init__(self, root, word_file, on_back_callback):
        self.root = root
        self.on_back_callback = on_back_callback  # 回调：返回选择界面
        self.root.title("GREat@背单词")
        self.root.geometry("760x860")
        self.root.resizable(False, False)
        self.word_file = word_file

        self.words = self.load_words()
        self.current_word = None

        self.create_ui()
        self.next_word()

    def load_words(self):
        words = []
        try:
            with open(self.word_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if "\t" in line:
                        w, m = line.split("\t", 1)
                    else:
                        parts = line.split(" ", 1)
                        if len(parts) < 2:
                            continue
                        w, m = parts
                    words.append((w.strip(), m.strip()))
        except Exception as e:
            messagebox.showerror("加载失败", f"读取单词文件失败：{str(e)}")
        return words

    def create_ui(self):
        # 顶部状态栏
        top_frame = tk.Frame(self.root, bg="#009E5F", height=100)
        top_frame.pack(fill=tk.X, anchor=tk.N)
        self.status_label = tk.Label(
            top_frame, text="剩余：0",
            bg="#009E5F", fg="yellow", font=("微软雅黑", 24, "bold")
        )
        self.status_label.pack(pady=30)

        # 单词 + 释义
        word_frame = tk.Frame(self.root, bg="white", height=250)
        word_frame.pack(fill=tk.X, pady=20)

        self.word_label = tk.Label(
            word_frame, text="", bg="white", font=("微软雅黑", 36, "bold")
        )
        self.word_label.pack(pady=15)

        line = tk.Frame(word_frame, bg="#CCCCCC", height=2)
        line.pack(fill=tk.X, padx=100)

        self.meaning_label = tk.Label(
            word_frame, text="", bg="white", font=("微软雅黑", 20)
        )
        self.meaning_label.pack(pady=20)

        # 按钮区域
        btn_frame = tk.Frame(self.root, bg="#F0F0F0")
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_rowconfigure(0, weight=1)

        self.btn_forget = tk.Button(
            btn_frame, text="我忘了", font=("微软雅黑", 22),
            bg="#FFFFFF", relief=tk.FLAT, command=self.on_forget
        )
        self.btn_forget.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

        self.btn_remember = tk.Button(
            btn_frame, text="我记得", font=("微软雅黑", 22),
            bg="#FFFFFF", relief=tk.FLAT, command=self.on_remember
        )
        self.btn_remember.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

        # ===================== 【新增】返回选择文件按钮 =====================
        self.back_btn = tk.Button(
            self.root, text="返回词库选择", font=("微软雅黑", 18),
            relief=tk.FLAT, bg="#E0E0E0", command=self.go_back
        )
        self.back_btn.pack(fill=tk.X, padx=20, pady=5)

        # 错题本按钮
        self.wrong_btn = tk.Button(
            self.root, text="打开错题本", font=("微软雅黑", 18),
            relief=tk.FLAT, bg="#E0E0E0", command=self.open_wrong_book
        )
        self.wrong_btn.pack(fill=tk.X, padx=20, pady=5)

        # 设置按钮
        self.set_btn = tk.Button(
            self.root, text="Settings", font=("微软雅黑", 18),
            relief=tk.FLAT, bg="#E0E0E0", command=self.open_settings
        )
        self.set_btn.pack(fill=tk.X, padx=20, pady=15)

    def next_word(self):
        if not self.words:
            self.word_label.config(text="🎉 背完啦！")
            self.meaning_label.config(text="恭喜完成学习")
            self.status_label.config(text="剩余：0")
            self.btn_forget.config(state=tk.DISABLED)
            self.btn_remember.config(state=tk.DISABLED)
            return

        self.current_word = self.words.pop()
        self.word_label.config(text=self.current_word[0])
        self.meaning_label.config(text=self.current_word[1])
        self.status_label.config(text=f"剩余：{len(self.words)}")

    def on_forget(self):
        add_wrong_word(self.current_word[0], self.current_word[1])
        self.words.insert(0, self.current_word)
        self.next_word()

    def on_remember(self):
        self.next_word()

    def open_wrong_book(self):
        wrong_words = load_wrong_words()
        if not wrong_words:
            messagebox.showinfo("错题本", "暂无错题！")
            return

        book_win = tk.Toplevel(self.root)
        book_win.title("错题本")
        book_win.geometry("600x500")

        text_area = scrolledtext.ScrolledText(book_win, font=("微软雅黑", 14))
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for word, meaning in wrong_words:
            text_area.insert(tk.END, f"📌 {word}\n{meaning}\n\n")

        text_area.config(state=tk.DISABLED)

    def open_settings(self):
        result = messagebox.askyesno("设置", "确定要清空所有错题本记录吗？")
        if result:
            clear_wrong_words()
            messagebox.showinfo("成功", "错题本已清空！")

    # 返回词库选择 
    def go_back(self):
        self.root.destroy()
        self.on_back_callback()