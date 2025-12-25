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
    """处理内容：注释转纯文本，代码进代码块"""
    lines = file_path.read_text(encoding='utf-8', errors='replace').splitlines()
    processed_parts = []
    current_code_block = []

    def flush_code():
        if current_code_block:
            # 关键：代码块前后必须有空行，确保 Jekyll 正确识别
            processed_parts.append("\n```python")
            processed_parts.extend(current_code_block)
            processed_parts.append("```\n")
            current_code_block.clear()

    for line in lines:
        # 匹配以 # 开头的行（允许前面有空格，适配缩进的代码注释）
        match = re.match(r'^\s*#\s?(.*)', line)
        if match:
            flush_code()
            comment_text = match.group(1)
            # 如果是空注释行，转为一个简单的换行
            processed_parts.append(comment_text if comment_text.strip() else "\n")
        else:
            # 普通代码行，收集起来
            current_code_block.append(line)
            
    flush_code()
    return "\n".join(processed_parts)

def build():
    if not SRC.exists():
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 统一页脚 (去掉 > 避免竖线)
    common_footer = [
        f"---/n"
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成详情页 ---
    markdown_segments = [f"# 🤔 Python 源码汇总\n", f"[⬅️ 返回首页](../README.md)\n"]

    for py in py_files:
        try:
            markdown_segments.append(f"### 📄 {py.name}")
            # 核心：确保标题和内容之间有空行
            markdown_segments.append("\n" + process_py_content(py))
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成主页 ---
    root_content = [
        "## 🚀 代码库主页\n",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 构建完成！代码块与注释已分离。")