# -*- coding: utf-8 -*-
import subprocess
import sys
import os

def run_coverage():
    """运行代码覆盖率统计"""
    # 检查是否安装coverage
    try:
        subprocess.run(["coverage", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ 未安装coverage模块，请先执行：pip install coverage")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ 未找到coverage命令，请先执行：pip install coverage")
        sys.exit(1)

    # 清理旧的覆盖率数据
    subprocess.run(["coverage", "erase"], capture_output=True)

    # 运行测试（以bei.py为例，可根据需要修改）
    test_cmd = ["coverage", "run", "--source=.", "bei.py", "test_words.txt"]
    print(f"🔍 运行测试命令：{' '.join(test_cmd)}")
    subprocess.run(test_cmd, capture_output=True)

    # 生成覆盖率报告
    print("\n📊 代码覆盖率报告：")
    subprocess.run(["coverage", "report", "-m"], check=True)

    # 生成HTML报告（可选）
    html_dir = "htmlcov"
    subprocess.run(["coverage", "html", "-d", html_dir], capture_output=True)
    print(f"\n✅ HTML报告已生成：{os.path.abspath(html_dir)}/index.html")

if __name__ == "__main__":
    run_coverage()