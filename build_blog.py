import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    name = p.stem
    if "序" in name: return (-1, name)
    m = re.match(r'^(\d+|[一二三四五六七八九十])', name)
    if not m: return (1, name)
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    content, code_acc = [], []
    def flush():
        if code_acc and any(l.strip() for l in code_acc):
            content.append(f"\n```python\n" + "\n".join(code_acc).strip() + "\n```\n")
        code_acc.clear()

    for line in p.read_text(encoding='utf-8').splitlines():
        # 匹配 # 及其后所有内容，保留注释内部的所有原始空格
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            # 获取 # 后的原始文本，不做 lstrip，直接保留源码缩进
            text = m.group(1)
            # 使用 <br> 强制换行，文字将按源码中的空格原样呈现
            content.append(f"{text}<br>")
        elif not line.strip():
            flush(); content.append("<br>")
        else:
            code_acc.append(line)
            
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    footer = [f"\n---\nmade by chanvel   |   {NOW}"]
    
    # 构建子页
    sub_body = ["[源代码汇总](../README.md)\n"]
    for py in py_files:
        sub_body.extend([f"### {py.stem}", process_py(py)])
    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')

    # 构建主页
    ROOT_MD.write_text("\n".join([f"[Python源代码](./python/README.md)"] + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 构建成功！已实现标题顶格对齐与正文精准缩进。")