import os
from pathlib import Path
from datetime import datetime

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC = Path('python')
ROOT_MD = Path('README.md')
SRC_MD = SRC / 'README.md'

def build():
    # 确保目录存在
    if not SRC.exists():
        print(f"⚠️ 找不到目录: {SRC}")
        SRC.mkdir(exist_ok=True)
        return

    py_files = sorted(SRC.glob('*.py'))
    
    # 定义通用的页脚，两个文件都能用
    common_footer = [
        f"\n---",
        f"> 更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    
    # --- 1. 生成 python/README.md (源码详情页) ---
    markdown_segments = [
        f"# 🤔 Python 源码汇总\n",
        f"[⬅️ 返回首页](../README.md)\n",
        "---\n"
    ]

    for py in py_files:
        try:
            code_content = py.read_text(encoding='utf-8', errors='replace')
            segment = [
                f"## 📄 {py.name}",
                '<div style="white-space: pre-wrap; word-wrap: break-word;">\n',
                f"```python\n{code_content}\n```",
                "</div>\n",
                "---\n"
            ]
            markdown_segments.extend(segment)
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    # 追加页脚
    markdown_segments.extend(common_footer)
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md (项目入口) ---
    # 使用列表加法 [+] 来合并内容，这样逻辑最清晰
    root_content = [
        "# 🚀 代码库主页\n",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
    ] + common_footer
    
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 构建完成！已同步 {len(py_files)} 个文件。")