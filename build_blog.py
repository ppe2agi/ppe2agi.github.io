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
    """
    核心逻辑：
    1. 识别 # 开头的注释，去掉 # 转为 Markdown 文本。
    2. 识别代码行，放入 ```python 块中。
    """
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
        print(f"⚠️ 找不到目录: {SRC}")
        SRC.mkdir(exist_ok=True)
        return

    # 获取所有 py 文件
    py_files = sorted(SRC.glob('*.py'))
    
    # 定义通用的页脚
    common_footer = [
        "\n---",
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成 python/README.md (源码详情页) ---
    # 使用 Front Matter 解决 Architect 主题排版
    markdown_segments = [
        "---",
        "layout: default",
        "title: Python 源代码详情",
        "---",
        "",
        f"[⬅️ 返回首页](../README.md)",
        ""
    ]

    for py in py_files:
        try:
            # 文件名作为三级标题，在 Architect 下更美观
            markdown_segments.append(f"### 📄 {py.name}\n")
            file_content = process_py_content(py)
            markdown_segments.append(file_content)
            print(f"✅ 已处理: {py.name}")
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md (项目入口) ---
    # 这里的 title 会显示在蓝色 Header 中，正文不再写 # 源代码
    root_content = [
        "---",
        "layout: default",
        "title: 源代码主页",
        "---",
        "",
        "### 📚 项目案例",
        f"- [📁 点击查看 Python 源代码](./python/README.md) (共 {len(py_files)} 个案例)",
        ""
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"\n✨ 构建完成！Architect 主题已适配。")