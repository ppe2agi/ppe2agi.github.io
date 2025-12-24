import os
from datetime import datetime

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 1. 生成根目录的总 README
with open('README.md', 'w', encoding='utf-8') as f:
    f.write("# 技术博客总入口\n") # 这里只用一个换行
    f.write("<sub>made by chanvel</sub>\n\n") # 这里再空两行进入下一段
    f.write("## 学习分类\n")
    f.write("- [🐍 Python 语言学习](./python/README.md)\n")
    f.write(f"\n> 最近更新: {current_date}")

# 2. 生成子目录的内容 (逻辑保持不变)
if os.path.exists('python'):
    with open('python/README.md', 'w', encoding='utf-8') as f:
        f.write("# Python 学习笔记\n\n")
        files = [file for file in os.listdir('python') if file.endswith('.py')]
        for file in files:
            file_path = os.path.join('python', file)
            f.write(f"## 文件名: {file}\n\n")
            with open(file_path, 'r', encoding='utf-8') as py_file:
                f.write("```python\n" + py_file.read() + "\n```\n\n---\n")

print(f"✅ 博客已成功更新，署名：chanvel，同步时间：{current_date}")