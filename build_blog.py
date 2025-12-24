import os
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

def build():
    # 1. 生成 CNAME 确保域名不丢失
    with open('CNAME', 'w', encoding='utf-8') as f:
        f.write(domain_name)

    # 2. 构造 README 内容
    content = [
        f"# 🏠 我的代码仓库\n\n",
        f"<sub>{author_info} | 本地最后同步: {current_date}</sub>\n\n",
        "## 🐍 Python 源码集锦\n\n---\n\n"
    ]
    
    source_dir = 'python'
    if os.path.exists(source_dir):
        # 按照文件名排序，确保页面整洁
        py_files = sorted([f for f in os.listdir(source_dir) if f.endswith('.py')])
        for file in py_files:
            content.append(f"### 📄 文件: {file}\n\n")
            with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_f:
                content.append(f"```python\n{py_f.read()}\n```\n\n---\n\n")
    
    # 3. 写入根目录 README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(content)

if __name__ == "__main__":
    build()
    print("✅ 本地 README.md 已更新，可以手动提交推送了。")