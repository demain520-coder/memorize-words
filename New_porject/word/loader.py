#读入单词
# -*- coding: utf-8 -*-
def load_words(file_path):
    words = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "\t" in line:
                w,m = line.split("\t",1)
                words.append((w.strip(), m.strip()))
    return words