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
    3. 识别纯空行，直接转为 Markdown 换行，不产生代码框。
    """
    lines = file_path.read_text(encoding='utf-8', errors='replace').splitlines()
    processed_parts = []
    current_code_block = []

    def flush_code():
        """将当前收集的代码行打包进代码块"""
        if current_code_block:
            # 只有当块内包含非空内容时才生成代码框
            if any(line.strip() for line in current_code_block):
                processed_parts.append("\n```python")
                processed_parts.extend(current_code_block)
                processed_parts.append("```\n")
            current_code_block.clear()

    for line in lines:
        # 1. 检查是否为注释行 (匹配开头的 #)
        comment_match = re.match(r'^\s*#\s?(.*)', line)
        
        if comment_match:
            flush_code()
            content = comment_match.group(1)
            # 如果是空注释则只换行，否则添加注释文字
            processed_parts.append(content if content.strip() else "\n")
            
        # 2. 检查是否为纯空行
        elif not line.strip():
            flush_code()
            processed_parts.append("") # 在 MD 中产生一个空行效果
            
        # 3. 否则视为普通代码行
        else:
            current_code_block.append(line)
            
    # 最后收尾
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
    
    # 定义通用的页脚 (修正了 \n 换行符)
    common_footer = [
        f"---\n",
        f"更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成 python/README.md (源码详情页) ---
    markdown_segments = [
        f"# 🤔 Python 源代码\n",
        f"[⬅️ 返回首页](../README.md)\n",
    ]

    for py in py_files:
        try:
            # 文件名作为三级标题 (###)，避免二级标题下的细横线
            markdown_segments.append(f"### 📄 {py.name}\n")
            
            # 处理内容：代码与注释分离
            file_content = process_py_content(py)
            markdown_segments.append(file_content)
            
            print(f"✅ 已处理: {py.name}")
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    # 拼接页脚并写入详情页
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md (项目入口) ---
    root_content = [
        f"# 源代码\n",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"\n✨ 构建完成！已同步 {len(list(SRC.glob('*.py')))} 个文件。")