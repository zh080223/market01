import random


def verify_code():
    s = []  # 定义列表 s
    for i in range(6):  # 生成6位随机数
        s.append(str(random.choice(range(10))))  # 将随机数转换为字符串并添加到列表 s
    return ''.join(s)
