import os
from pathlib import Path
from datetime import datetime
import re

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC = Path('python')
ROOT_MD = Path('README.md')
SRC_MD = SRC / 'README.md'

def process_py_content(file_path):
    lines = file_path.read_text(encoding='utf-8', errors='replace').splitlines()
    processed_parts = []
    current_code_block = []

    def flush_code():
        if current_code_block:
            if any(line.strip() for line in current_code_block):
                processed_parts.append("\n```python")
                processed_parts.extend(current_code_block)
                processed_parts.append("```\n")
            current_code_block.clear()

    for line in lines:
        comment_match = re.match(r'^\s*#\s?(.*)', line)
        if comment_match:
            flush_code()
            content = comment_match.group(1)
            processed_parts.append(content if content.strip() else "\n")
        elif not line.strip():
            flush_code()
            processed_parts.append("") 
        else:
            current_code_block.append(line)
            
    flush_code()
    return "\n".join(processed_parts)

def build():
    if not SRC.exists():
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 通用页脚
    common_footer = [
        "\n---",
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成子目录详情页 ---
    # 删掉一级标题，详情页正文从二级标题开始
    sub_md = [
        f"## 📄 Python 源代码详情\n", # 改为二级
        f"[⬅️ 返回首页](../README.md)\n",
    ]

    for py in py_files:
        try:
            sub_md.append(f"### 📄 {py.name}\n") # 文件名用三级
            sub_md.append(process_py_content(py))
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    sub_md.extend(common_footer)
    SRC_MD.write_text('\n'.join(sub_md), encoding='utf-8')

    # --- 2. 生成根目录首页 ---
    # 核心修改：首页不再使用一级标题 #
    root_md = [
        f"## 📚 源代码目录\n", # 这里改用二级标题
        f"- [📁 点击查看 Python 源代码案例](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_md), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"\n✨ 构建完成！已适配固定 Title 配置。")