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
    
    # --- 1. 生成 python/README.md (源码详情页) ---
    # 头部内容
    markdown_segments = [
        f"# 🤔 Python 源码汇总\n",
        f"[⬅️ 返回首页](../README.md)\n",
        "---\n"
    ]

    # 中间内容：循环添加源码
    for py in py_files:
        try:
            code_content = py.read_text(encoding='utf-8', errors='replace')
            segment = [
                f"## 📄 {py.name}",
                # 针对 GitHub Pages 的自动换行容器
                '<div style="white-space: pre-wrap; word-wrap: break-word;">\n',
                f"```python\n{code_content}\n```",
                "</div>\n",
                "---\n"
            ]
            markdown_segments.extend(segment)
        except Exception as e:
            print(f"❌ 读取 {py.name} 失败: {e}")
    
    # 尾部内容：使用 extend 而不是重新赋值
    footer = [
        f"\n> 更新时间: {NOW}  ",
        "made by **chanvel**"
    ]
    markdown_segments.extend(footer)

    # 一次性写入文件
    SRC_MD.write_text('\n'.join(markdown_segments), encoding='utf-8')

    # --- 2. 生成根目录 README.md (项目入口) ---
    root_content = [
        "# 🚀 代码库",
        f"- [📁 Python 源码详情](./python/README.md) ({len(py_files)} 个案例文件)\n",
        "---",
        f"最后同步日期: `{NOW}`  ",
        "made by **chanvel**"
    ]
    ROOT_MD.write_text('\n'.join(root_content), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✅ 构建完成！已同步 {len(list(SRC.glob('*.py')))} 个文件到 Markdown。")