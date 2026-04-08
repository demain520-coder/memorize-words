# -*- coding: utf-8 -*-
import sys
import os

def fix_word_file(input_path, output_path=None):
    """
    修复单词文件格式：
    1. 去除空行、注释行
    2. 统一格式为「单词\t释义」
    3. 去除多余空格
    """
    if not output_path:
        output_path = input_path + ".fixed"

    fixed_lines = []
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith("#"):
                    continue
                # 分割单词和释义
                if "\t" in line:
                    word, meaning = line.split("\t", 1)
                else:
                    parts = line.split(maxsplit=1)
                    if len(parts) < 2:
                        print(f"警告：第{line_num}行格式错误，跳过：{line}")
                        continue
                    word, meaning = parts
                # 去除多余空格
                word = word.strip()
                meaning = meaning.strip()
                fixed_lines.append(f"{word}\t{meaning}")

        # 写入修复后的文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(fixed_lines))
        print(f"✅ 修复完成！共处理 {len(fixed_lines)} 个单词")
        print(f"✅ 输出文件：{output_path}")
    except Exception as e:
        print(f"❌ 修复失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 fix.py [待修复单词文件] [输出文件(可选)]")
        print("示例: python3 fix.py 08red/11.txt 08red/11.fixed.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    fix_word_file(input_file, output_file)