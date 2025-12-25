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
    """提取 Python 文件内容并转换为 MD"""
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
    # 确保目录存在
    if not SRC.exists():
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 定义通用的页脚
    common_footer = "\n---\n更新时间: " + NOW + "  \nmade by **chanvel**"
    
    # --- 1. 生成子目录 python/README.md ---
    # 使用字符串直接拼接确保格式最稳固
    sub_md_header = "---\nlayout: default\ntitle: Python 源码详情\n---\n\n"
    sub_md_body = "[⬅️ 返回首页](../README.md)\n\n"

    for py in py_files:
        try:
            sub_md_body += "### 📄 " + py.name + "\n"
            sub_md_body += process_py_content(py) + "\n"
            print("✅ 已处理: " + py.name)
        except Exception as e:
            print("❌ 错误: " + str(e))
    
    SRC_MD.write_text(sub_md_header + sub_md_body + common_footer, encoding='utf-8')

    # --- 2. 生成根目录 README.md ---
    # 严格遵循 YAML Front Matter 规范
    root_md_header = "---\nlayout: default\ntitle: 源代码主页\n---\n\n"
    root_md_body = "### 📚 项目案例\n"
    root_md_body += "- [📁 点击查看 Python 源代码](./python/README.md) (共 " + str(len(py_files)) + " 个案例)\n"
    
    ROOT_MD.write_text(root_md_header + root_md_body + common_footer, encoding='utf-8')

if __name__ == "__main__":
    build()
    print("\n✨ 构建成功！请提交代码并在 GitHub 仓库的 'Actions' 页面观察构建进度。")