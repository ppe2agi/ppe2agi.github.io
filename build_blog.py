import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
# 获取当前时间
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    """智能排序：支持数字和中文序号，不改动原始文件名"""
    m = re.match(r'^(\d+|[一二三四五六七八九十])', p.stem)
    if not m: return (1, p.stem)
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    """提取注释与代码块"""
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
    # 使用自定义排序
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    
    # 修改页脚样式
    footer = [f"\n---\nmade by chanvel  |  {NOW}"]
    
    # 1. 详情页 (python/README.md)
    # p.stem 会保留所有原始字符，包括英文空格
    sub_body = [f"[源代码汇总](../README.md)\n"]
    for py in py_files:
        sub_body.extend([f"### {py.stem}", process_py(py)])
    SRC_MD.write_text("\n".join(sub_body + footer), encoding='utf-8')

    # 2. 主页 (README.md)
    root_body = [f"[Python源代码](./python/README.md)"]
    ROOT_MD.write_text("\n".join(root_body + footer), encoding='utf-8')

if __name__ == "__main__":
    build()
    print(f"✨ 构建成功！英文空格已保留，页脚样式已更新。")