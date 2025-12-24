import os
import shutil
from datetime import datetime

# === 配置信息 ===
current_date = datetime.now().strftime('%Y-%m-%d')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

def build():
    # 1. 彻底清理并重建 docs 文件夹，确保环境纯净
    if os.path.exists('docs'):
        shutil.rmtree('docs')
    os.makedirs('docs/python', exist_ok=True)

    # 2. 生成 CNAME (保持自定义域名绑定)
    with open('docs/CNAME', 'w', encoding='utf-8') as f:
        f.write(domain_name)

    # 3. 生成首页 index.md
    with open('docs/index.md', 'w', encoding='utf-8') as f:
        f.write(f"# 🏠 我的代码库总览\n\n")
        f.write(f"<sub>{author_info} | 最近更新: {current_date}</sub>\n\n")
        f.write("## 快速导航\n")
        f.write("- [🤔 Python 语言案例库](./python/index.md)\n")

    # 4. 提取根目录 python/ 文件夹下的源码
    source_dir = 'python'
    dest_file = 'docs/python/index.md'
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        f.write(f"# 🤔 Python 语言案例\n\n")
        f.write(f"<sub>此页面由脚本自动生成，收录了 `{source_dir}/` 目录下的所有源码。</sub>\n\n---\n\n")
        
        if os.path.exists(source_dir):
            py_files = [file for file in os.listdir(source_dir) if file.endswith('.py')]
            if not py_files:
                f.write("目前该分类下暂无代码文件。\n")
            else:
                for file in py_files:
                    f.write(f"### 📄 案例: {file}\n\n")
                    with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_content:
                        f.write(f"```python\n{py_content.read()}\n```\n\n---\n\n")
        else:
            f.write("未找到 python 源码文件夹。\n")

if __name__ == "__main__":
    build()
    print("✅ 文档已成功构建到 docs/ 目录")