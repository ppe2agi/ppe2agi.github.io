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
    """提取 Python 内容并转为 MD"""
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
    
    # --- 1. 生成 python/README.md (详情页) ---
    # 全部改为二级标题，避免被 Cayman 抓取到顶部
    markdown_segments = [
        f"## 🤔 Python 源代码详情\n",
        f"[⬅️ 返回首页](../README.md)\n",
    ]

    for py in py_files:
        try:
            # 文件名使用三级标题，层次分明
            markdown_segments.append(f"### 📄 {py.name}\n")
            markdown_segments.append(process_py_content(py))
            print(f"✅ 已同步: {py.name}")
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md (首页) ---
    # 将原来的 # 源代码 换成了 ## 源代码
    root_content = [
        f"## 源代码\n",
        f"- [📁 Python 源代码案例](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"\n✨ 构建完成！标题已降级为二级。")