import os
import shutil
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

# === 1. 清理并初始化 docs 目录 ===
if os.path.exists('docs'):
    shutil.rmtree('docs') # 彻底删除旧的，防止目录混乱
os.makedirs('docs/python')

# === 2. 生成 CNAME ===
with open('docs/CNAME', 'w', encoding='utf-8') as f:
    f.write(domain_name)

# === 3. 生成首页 index.md ===
with open('docs/index.md', 'w', encoding='utf-8') as f:
    f.write(f"# 欢迎来到我的代码库\n\n")
    f.write(f"<sub><font color='#888'>{author_info} | 最近更新: {current_date}</font></sub>\n\n")
    f.write("### 内容分类\n")
    f.write("- [🤔 Python 语言](./python/index.md)\n")

# === 4. 处理 python 文件夹下的源码 ===
source_dir = 'python' # 指向根目录下的 python 文件夹
dest_file = 'docs/python/index.md'

with open(dest_file, 'w', encoding='utf-8') as f:
    f.write(f"# 🤔 Python 语言\n")
    f.write(f"<sub><font color='#888'>{author_info}</font></sub>\n\n")
    
    if os.path.exists(source_dir):
        # 过滤出 .py 文件
        py_files = [file for file in os.listdir(source_dir) if file.endswith('.py')]
        
        if not py_files:
            f.write("目前暂无代码文件。\n")
        else:
            for file in py_files:
                f.write(f"### 📄 文件名: {file}\n\n")
                with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_content:
                    f.write("```python\n" + py_content.read() + "\n```\n\n---\n\n")

print(f"✅ 目录已重构，docs 文件夹已准备就绪。")