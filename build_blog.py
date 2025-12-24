import os

def generate_blog():
    # 博客首页标题
    content = "# 我的 Python 学习自动化博客\n\n"
    content += "这是由脚本自动生成的项目文档，更新时间自动同步。\n\n"

    # 遍历当前目录下所有的文件
    for filename in sorted(os.listdir('.')):
        # 排除掉脚本自身和隐藏文件
        if filename.endswith('.py') and filename != 'build_blog.py':
            content += f"## 脚本：{filename}\n"
            content += "```python\n"
            
            # 读取 .py 文件内容并写入 md
            with open(filename, 'r', encoding='utf-8') as f:
                content += f.read()
            
            content += "\n```\n\n---\n\n"

    # 将所有内容写入 README.md 或 index.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 博客已自动更新到 README.md")

if __name__ == "__main__":
    generate_blog()