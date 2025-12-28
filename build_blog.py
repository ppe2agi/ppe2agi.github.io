import re
from pathlib import Path
from datetime import datetime

# --- 配置 ---
# 获取当前时间
NOW = datetime.now().strftime('%Y-%m-%d %H:%M')
SRC, ROOT_MD, SRC_MD = Path('python'), Path('README.md'), Path('python/README.md')
CN_MAP = {c: i for i, c in enumerate('一二三四五六七八九十', 1)}

def get_sort_key(p):
    name = p.stem
    m = re.match(r'^(\d+|[一二三四五六七八九十])', name)
    
    # 元组第一位决定大类：
    # -1: 包含“序”的文件 (最高)
    #  0: 带数字/中文序号的文件 (中等)
    #  1: 普通文件 (最低)    
    if "序" in name: return (-1, name)
    if not m: return (1, name)
    
    val = m.group(1)
    return (0, int(val) if val.isdigit() else CN_MAP.get(val, 99))

def process_py(p):
    content, code_acc = [], []
    def flush():
        if code_acc and any(l.strip() for l in code_acc):
            content.append(f"\n```python\n" + "\n".join(code_acc) + "\n```\n")
        code_acc.clear()

    for line in p.read_text(encoding='utf-8').splitlines():
        # 匹配注释行，保留原始空格
        m = re.match(r'^\s*#\s?(.*)', line)
        if m:
            flush()
            text = m.group(1)
            
            # 1. 处理“粗线”问题：如果是连续的 = 或 -，统一转为 Markdown 细分割线
            if re.match(r'^[=\-]{3,}$', text.strip()):
                content.append("\n---\n")
            
            # 2. 正常文字排版：末尾加 <br> 确保 GitHub 强制换行且不合并段落
            # 这样你在 py 里写几行，GitHub 预览就是几行
            else:
                content.append(f"{text}<br>") 
        
        elif not line.strip():
            flush()
            content.append("<br>") # 空行也用 <br> 占位，保持间距
        else:
            code_acc.append(line)
            
    flush()
    return "\n".join(content)

def build():
    SRC.mkdir(exist_ok=True)
    # 使用自定义排序
    py_files = sorted(SRC.glob('*.py'), key=get_sort_key)
    
    # 修改页脚样式
    footer = [f"\n---\nmade by chanvel   |   {NOW}"]
    
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
    print(f"✨ 构建成功！已调整换行逻辑，防止内容合并。")