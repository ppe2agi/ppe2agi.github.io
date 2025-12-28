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
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            text = m.group(1)
            stripped = text.lstrip()
            
            # 1. 分隔线：确保前后空行，防止文字变粗
            if re.match(r'^[=\-]{3,}$', stripped):
                content.append("\n---\n")
            
            # 2. 标题行：顶格，序号后补全角空格
            elif re.match(r'^(\d+[\.、\s]|\d+(\.\d+)+|[\u4e00-\u9fa5]+[、]|【|-|\*)', stripped):
                h = re.match(r'^(\d+[\.、]|\d+(\.\d+)+|[\u4e00-\u9fa5]+[、])', stripped)
                if h:
                    pre, rest = h.group(1).rstrip(), stripped[h.end():].lstrip()
                    # 序号后补一个全角空格 '　'，能让标题文字的起始点与缩进后的正文完美对齐
                    content.append(f"{pre}　{rest}<br>")
                else:
                    content.append(f"{stripped}<br>")
            
            # 3. 正文行：精准使用两个全角空格缩进
            else:
                content.append(f"　　{stripped}<br>" if stripped else "<br>")
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