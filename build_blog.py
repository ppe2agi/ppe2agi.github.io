import os
from datetime import datetime

# === 配置 ===
current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
author_info = "made by chanvel"
domain_name = "blog.ppe2agi.qzz.io"

def build():
    # 1. 强制生成 CNAME
    with open('CNAME', 'w', encoding='utf-8') as f:
        f.write(domain_name)

    # 2. 准备 README 内容
    lines = [
        f"# 🏠 我的 Python 代码仓库总目录\n\n",
        f"<sub>{author_info} | 本地最后同步: {current_date}</sub>\n\n",
        "## 🐍 源码清单\n\n",
        "这里记录了所有自动提取的 Python 案例源码：\n\n---\n\n"
    ]
    
    source_dir = 'python'
    if os.path.exists(source_dir):
        # 获取所有 .py 文件并排序
        files = sorted([f for f in os.listdir(source_dir) if f.endswith('.py')])
        
        if not files:
            lines.append("> 目前文件夹内暂无代码文件。\n")
        else:
            for file in files:
                lines.append(f"### 📄 {file}\n\n")
                # 读取源码内容
                with open(os.path.join(source_dir, file), 'r', encoding='utf-8') as py_f:
                    code_content = py_f.read()
                    lines.append(f"```python\n{code_content}\n```\n\n---\n\n")
    
    # 3. 写入 README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    build()
    print("✅ 成功！README.md 已更新为最新总目录。")