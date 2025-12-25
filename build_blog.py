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
    """提取 Python 内容并转换为 Markdown，确保注释与代码块层级正确"""
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
        print(f"⚠️ 找不到目录: {SRC}")
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 通用页脚：使用 --- 触发 CSS 中定义的细线样式
    common_footer = [
        "\n---",
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成子目录 python/README.md (详情页) ---
    # 核心修复：显式包含 YAML Front Matter 确保子目录应用自定义布局
    sub_md = [
        "---",
        "layout: default",
        "---",
        "",
        f"[⬅️ 源代码汇总](../README.md)\n",
    ]

    for py in py_
