#主入口
# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ui.window import WordApp


def scan_all_vocab_files():
    VOCAB_FOLDER = r"E:\git\memorize-words\vocab"
    if not os.path.exists(VOCAB_FOLDER):
        messagebox.showerror("错误", f"目录不存在：\n{VOCAB_FOLDER}")
        return []
    files = []
    for name in os.listdir(VOCAB_FOLDER):
        if name.lower().endswith(".txt"):
            full_path = os.path.join(VOCAB_FOLDER, name)
            files.append((name, full_path))
    return files


def show_select_window(files):
    if not files:
        messagebox.showwarning("提示", "未找到任何单词文件！")
        return None

    win = tk.Tk()
    win.title("选择词库")
    win.geometry("550x350")
    win.resizable(False, False)

    tk.Label(win, text="请选择要背诵的单词文件", font=("微软雅黑", 14)).pack(pady=10)
    listbox = tk.Listbox(win, font=("微软雅黑", 12), height=10)

    for display_name, full_path in files:
        listbox.insert(tk.END, display_name)

    listbox.pack(fill=tk.BOTH, expand=True, padx=20)
    selected = [None]

    def confirm():
        idx = listbox.curselection()
        if not idx:
            messagebox.showwarning("提示", "请先选择一个文件")
            return
        selected[0] = files[idx[0]][1]
        win.destroy()

    ttk.Button(win, text="确认选择", command=confirm).pack(pady=12)
    win.mainloop()
    return selected[0]


def start_app():
    vocab_list = scan_all_vocab_files()
    selected_file = show_select_window(vocab_list)
    if not selected_file:
        sys.exit()

    main_win = tk.Tk()
    app = WordApp(main_win, selected_file, start_app)
    main_win.mainloop()


if __name__ == "__main__":
    start_app()