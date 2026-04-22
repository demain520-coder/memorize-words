#主入口
# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ui.window import WordApp


def scan_all_vocab_files():
    # 使用相对路径，基于当前文件位置
    VOCAB_FOLDER = os.path.join(os.path.dirname(__file__), "vocab")
    if not os.path.exists(VOCAB_FOLDER):
        # 如果目录不存在，创建它
        os.makedirs(VOCAB_FOLDER, exist_ok=True)

    files = []
    for name in os.listdir(VOCAB_FOLDER):
        if name.lower().endswith(".txt"):
            full_path = os.path.join(VOCAB_FOLDER, name)
            files.append((name, full_path))
    return files


def show_select_window(files):
    if not files:
        messagebox.showwarning("提示", "未找到任何单词文件！")
        return None, False

    win = tk.Tk()
    win.title("选择词库")
    win.geometry("550x400")
    win.resizable(False, False)

    tk.Label(win, text="请选择要背诵的单词文件", font=("微软雅黑", 14)).pack(pady=10)
    listbox = tk.Listbox(win, font=("微软雅黑", 12), height=10)

    for display_name, full_path in files:
        listbox.insert(tk.END, display_name)

    listbox.pack(fill=tk.BOTH, expand=True, padx=20)
    
    # 添加乱序选项
    shuffle_var = tk.BooleanVar(value=False)
    shuffle_checkbox = tk.Checkbutton(win, text="乱序背单词", font=("微软雅黑", 12), variable=shuffle_var)
    shuffle_checkbox.pack(pady=10)
    
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
    return selected[0], shuffle_var.get()


def start_app():
    vocab_list = scan_all_vocab_files()
    selected_file, shuffle = show_select_window(vocab_list)
    if not selected_file:
        sys.exit()

    main_win = tk.Tk()
    app = WordApp(main_win, selected_file, start_app, shuffle)
    main_win.mainloop()


if __name__ == "__main__":
    start_app()