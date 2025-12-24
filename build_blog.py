import os
from datetime import datetime

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"

# 1. 生成根目录的总 README.md
with open('README.md', 'w', encoding='utf-8') as f:
    # 标题下换行，并使用 <font color="#888"> 设置为浅灰色
    f.write(f"<sub><font color='#888'>{author_info} | 最近更新: {current_date}</font></sub>\n\n")
    f.write("- [🤔 Python 语言](./python/README.md)\n")

# 2. 生成子目录的内容
if not os.path.exists('python'):
    os.makedirs('python')

with open('python/README.md', 'w', encoding='utf-8') as f:
    # 子目录也保持同样的低调灰色风格
    f.write(f"# 🤔 Python 语言\n")
    f.write(f"<sub><font color='#888'>{author_info}</font></sub>\n\n")
    f.write("这里记录了从 .py 文件中自动提取的源码和案例。\n\n---\n\n")
    
    files = [file for file in os.listdir('python') if file.endswith('.py')]
    
    if not files:
        f.write("目前该分类下暂无代码文件。\n")
    else:
        for file in files:
            file_path = os.path.join('python', file)
            f.write(f"### 📄 文件名: {file}\n\n")
            with open(file_path, 'r', encoding='utf-8') as py_content:
                f.write("```python\n" + py_content.read() + "\n```\n\n---\n\n")

print(f"✅ 样式已优化：副标题已改为浅灰色（#888），更新日期：{current_date}")