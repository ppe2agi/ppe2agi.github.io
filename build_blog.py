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
    
    # 1. 生成 python/README.md (源码详情页)
    markdown_segments = [
        f"# 🐍 Python 源码汇总\n",
        f"> 更新时间: {NOW}  ",
        f"[⬅️ 返回首页](../README.md)\n",
        "---\n"
    ]

    for py in py_files:
        try:
            # 读取代码，增加容错处理
            code_content = py.read_text(encoding='utf-8', errors='replace')
            
            segment = [
                f"## 📄 {py.name}",
                # 使用 HTML 容器包裹代码块，强制渲染时长代码换行
                '<div style="white-space: pre-wrap; word-wrap: break-word;">\n',
                f"```python\n{code_content}\n```",
                "</div>\n",
                "---\n"
            ]
            markdown_segments.extend(segment)
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")

    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # 2. 生成根目录 README.md (项目入口)
    root_content = [
        "# 🚀 代码库项目索引\n",
        f"最后同步日期: `{NOW}`\n",
        "## 目录导航",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
        "---",
        "Tip: 在 VS Code 中预览此文档可按 `Ctrl+Shift+V`。"
    ]
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 构建完成！已处理 {len(list(SRC.glob('*.py')))} 个文件。")