import os
from datetime import datetime

# 获取当前日期，确保每次同步时日期自动更新
current_date = datetime.now().strftime('%Y-%m-%d')

# 署名信息
author_info = "made by chanvel"

# 1. 生成根目录的总 README.md
with open('README.md', 'w', encoding='utf-8') as f:
    # 将标题、署名、日期合并在同一行，并位于 GitHub 标题下划线上方
    f.write(f"# 技术博客总入口 <sub>{author_info} | 最近更新: {current_date}</sub>\n\n")
    
    f.write("## 学习分类\n")
    # 链接到子目录的 README
    f.write("- [🐍 Python 语言学习](./python/README.md)\n")

# 2. 生成 python/ 目录的子 README.md
# 确保文件夹存在，避免 git add 时报错
if not os.path.exists('python'):
    os.makedirs('python')

with open('python/README.md', 'w', encoding='utf-8') as f:
    f.write(f"# 🐍 Python 学习笔记 <sub>{author_info}</sub>\n\n")
    f.write("这里记录了从 .py 文件中自动提取的详细源码和案例。\n\n")
    f.write("---\n\n")
    
    # 自动遍历 python 目录下的所有 .py 文件
    files = [file for file in os.listdir('python') if file.endswith('.py')]
    
    if not files:
        f.write("目前该分类下暂无代码文件。\n")
    else:
        for file in files:
            file_path = os.path.join('python', file)
            f.write(f"### 📄 文件名: {file}\n\n")
            
            # 读取 .py 源码内容并转为 Markdown 代码块
            try:
                with open(file_path, 'r', encoding='utf-8') as py_file:
                    code_content = py_file.read()
                    f.write("```python\n")
                    f.write(code_content)
                    f.write("\n```\n\n")
                    f.write("---\n\n")
            except Exception as e:
                f.write(f"读取文件时出错: {e}\n\n")

print(f"✅ 成功更新总入口及子目录博客内容。")
print(f"🕒 当前日期: {current_date} | 署名: {author_info}")