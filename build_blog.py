import os
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

def build():
    # 1. 生成 CNAME
    with open('CNAME', 'w', encoding='utf-8') as f:
        f.write(domain_name)

    # 2. 生成根目录 README.md (这就是你的网页主页)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(f"# 🏠 我的代码库\n\n")
        f.write(f"<sub>{author_info} | 更新日期: {current_date}</sub>\n\n")
        f.write("## 🐍 Python 案例源码\n\n---\n\n")
        
        source_dir = 'python'
        if os.path.exists(source_dir):
            py_files = [file for file in os.listdir(source_dir) if file.endswith('.py')]
            for file in py_files:
                f.write(f"### 📄 {file}\n\n")
                with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_content:
                    f.write(f"```python\n{py_content.read()}\n```\n\n---\n\n")

if __name__ == "__main__":
    build()
    print("✅ 极简 README.md 已在根目录更新")