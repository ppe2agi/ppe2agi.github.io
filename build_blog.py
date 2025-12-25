import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    """排序：识别数字和中文序号，保留空格"""
    m = re.match(r'^(\d+|[一二三四五六七八九十])', p.stem)
    if not m: return (1, p.stem)
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    """解析代码与注释"""
    content, code_acc = [], []
    def flush():
        if code_acc and any(l.strip() for l in code_acc):
            content.extend(["\n```python", *code_acc, "```\n"])
        code_acc.clear()

    for line in p.read_text(encoding='utf-8', errors='replace').splitlines():
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            content.append(m.group(1) or "\n")
        elif not line.strip():
            flush()
            content.append("")
        else:
            code_acc.append(line)
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    footer = [f"\n\n更新时间: {NOW}", "made by **chanvel**"]
    
    # 1. 详情页 (python/README.md)：去掉段落间的 ---
    sub_body = ["# 📄 源代码详情", f"\n[⬅️ 返回主页](../README.md)\n"]
    for py in py_files:
        sub_body.extend([f"### {py.stem}", process_py(py)])
    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')

    # 2. 主页 (README.md)：仅保留连接到详情页的入口
    root_body = [
        "# 📚 项目主页",
        f"\n- [📁 点击查看 Python 源代码详情 ({len(py_files)})](./python/README.md)"
    ]
    ROOT_MD.write_text("\n".join(root_body + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 构建完成：主页已简化，详情页内容已同步。")