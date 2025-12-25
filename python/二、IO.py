# #!/usr/bin python 
# #!：是一个特殊符号组合，告诉 Linux 内核，接下来的路径是执行本文件的解释器。
# /usr/bin/：这是存放系统命令的目录。
# python：这是你指定的解释器名称。
# 写脚本的时候，放在第一行，类似windows上的echo。

print('hello,world!')
# print()函数，可以打印多个字符串，中间用','隔开，','会在输出后形成空格，可以可以打印计算,比如下面的输出都是2,加入字符串查看区别。
print(1+1)
print(2)
print('1+1=',1+1)
print('1 + 1 =',1+1)

# name=input()
# 进入交互模式，输入了什么，输出什么，也可以增加print()会更有意思。
name=input('请输入您的名字')
print('你好',name)

# input()和output()，构成了最基本的IO。
# 关于注释，最前面 #和一个空格 ，这是标准样式，快捷键是 ctrl+/。