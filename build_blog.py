import os
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

def build():
    # 1. 确保 CNAME 存在
    with open('CNAME', 'w', encoding='utf-8') as f:
        f.write(domain_name)

    # 2. 生成根目录 README.md (总目录)
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(f"# 🏠 我的自动化文档首页\n\n")
        f.write(f"<sub>{author_info} | 更新时间: {current_date}</sub>\n\n")
        f.write("### 📂 内容分类\n")
        f.write("- [🤔 Python 语言源码库](./python/README.md) —— 点击查看所有代码案例\n")

    # 3. 生成 python/README.md (源码详情页)
    source_dir = 'python'
    if not os.path.exists(source_dir):
        os.makedirs(source_dir)
        
    py_files = sorted([f for f in os.listdir(source_dir) if f.endswith('.py')])
    
    with open(os.path.join(source_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f"# 🤔 Python 源码详情\n\n")
        f.write(f"[⬅️ 返回首页](../README.md)\n\n---\n\n")
        
        if not py_files:
            f.write("> 暂无代码文件。\n")
        else:
            for file in py_files:
                f.write(f"### 📄 案例：{file}\n\n")
                with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_f:
                    f.write(f"```python\n{py_f.read()}\n```\n\n---\n\n")

if __name__ == "__main__":
    build()
    print("✅ 首页与源码详情页已同步更新完成！")