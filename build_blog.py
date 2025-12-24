import os

# 1. 生成根目录的总 README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write("# 我的技术博客总入口\n\n")
    f.write("## 学习分类\n")
    f.write("- [🐍 Python 语言学习](./python/README.md)\n")
    f.write("\n> 最近更新: 2025-12-24")

# 2. 生成 python/ 目录的子 README
if os.path.exists('python'):
    with open('python/README.md', 'w', encoding='utf-8') as f:
        f.write("# Python 学习笔记\n\n")
        f.write("这里记录了 Python 的详细语法和案例。\n")
        # 自动列出 python 目录下的文件
        files = os.listdir('python')
        for file in files:
            if file.endswith('.py'):
                f.write(f"- {file}\n")

print("✅ 博客已自动更新到 README.md 和 python/README.md")