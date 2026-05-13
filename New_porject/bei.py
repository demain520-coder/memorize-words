# -*- coding: utf-8 -*-
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ui.window import WordApp
# 【新增】导入进度相关函数
from word.progress import load_progress, has_valid_progress
# 【新增】导入单词读取工具
from word.loader import load_words


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


# 【修改】返回值增加 open_mode 模式标记
def show_select_window(files):
    if not files:
        messagebox.showwarning("提示", "未找到任何单词文件！")
        # 【修改】多返回一个模式字段
        return None, False, "normal"

    win = tk.Tk()
    win.title("选择词库")
    # 【修改】窗口高度加大
    win.geometry("550x480")
    win.resizable(False, False)

    tk.Label(win, text="请选择要背诵的单词文件", font=("微软雅黑", 14)).pack(pady=10)
    listbox = tk.Listbox(win, font=("微软雅黑", 12), height=10)

    for display_name, full_path in files:
        listbox.insert(tk.END, display_name)

    listbox.pack(fill=tk.BOTH, expand=True, padx=20)

    # 添加乱序选项
    shuffle_var = tk.BooleanVar(value=False)
    shuffle_checkbox = tk.Checkbutton(win, text="乱序背单词", font=("微软雅黑", 12), variable=shuffle_var)
    shuffle_checkbox.pack(pady=5)

    selected = [None]
    # 【新增】标记打开模式：正常/恢复上次
    open_mode = ["normal"]

    def confirm():
        idx = listbox.curselection()
        if not idx:
            messagebox.showwarning("提示", "请先选择一个文件")
            return
        selected[0] = files[idx[0]][1]
        open_mode[0] = "normal"
        win.destroy()

    # 【新增】打开上次背诵按钮点击事件
    def open_last():
        if not has_valid_progress():
            messagebox.showinfo("提示", "暂无有效背诵记录")
            return
        open_mode[0] = "resume"
        win.destroy()

    # 【新增】按钮容器，放两个按钮
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    ttk.Button(btn_frame, text="确认选择", command=confirm).grid(row=0, column=0, padx=10)
    # 【新增】打开上次背诵按钮
    ttk.Button(btn_frame, text="打开上次背诵", command=open_last).grid(row=0, column=1, padx=10)

    win.mainloop()
    # 【修改】多返回模式
    return selected[0], shuffle_var.get(), open_mode[0]


def start_app():
    vocab_list = scan_all_vocab_files()
    # 【修改】接收第三个返回值：打开模式
    selected_file, shuffle, open_mode = show_select_window(vocab_list)

    # 【新增】分支：直接打开上次进度
    if open_mode == "resume":
        data = load_progress()
        last_file = data["last_word_file"]
        remaining = data["remaining_words"]
        main_win = tk.Tk()
        # 【修改】传入剩余单词列表
        app = WordApp(main_win, last_file, remaining, start_app)
        main_win.mainloop()
        return

    if not selected_file:
        sys.exit()

    # 【新增】正常选词时，检测是否有同文件历史进度
    data = load_progress()
    resume_words = None
    if data and data.get("last_word_file") == selected_file:
        remaining = data.get("remaining_words", [])
        if len(remaining) > 0:
            # 【新增】询问是否恢复
            if messagebox.askyesno("恢复进度", "检测到上次背诵记录，是否恢复？"):
                resume_words = remaining

    # 加载原始单词表
    all_words = load_words(selected_file)
    if shuffle:
        import random
        random.shuffle(all_words)

    # 【新增】有恢复进度就用旧的，没有就用全新单词表
    final_words = resume_words if resume_words is not None else all_words

    main_win = tk.Tk()
    # 【修改】传入最终单词列表
    app = WordApp(main_win, selected_file, final_words, start_app, shuffle)
    main_win.mainloop()


if __name__ == "__main__":
    start_app()