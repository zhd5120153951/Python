'''
@FileName   :生成器.py
@Description:生成器的作用是把循环的操作对象或者变量，只在内存中存在一份，而不是全部创建
@Date       :2024/04/13 15:13:45
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''

# 生成器函数


def func(str):
    print("进入生成器...")
    yield 123
    print("又进入生成器...")
    yield "daito"
    print("又又进入生成器")
    yield ["int", "str"]


gen = func("hello")  # 表示返回一个生成器对象
for item in gen:
    print(item)

# 用处


def create_big_num(maxNum):
    num = 1
    while True:
        yield num
        if num > maxNum:
            return
        num += 1


gen_obj = create_big_num(100000)
for item in gen_obj:
    print(item)
