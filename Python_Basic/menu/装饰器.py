'''
@FileName   :装饰器.py
@Description:装饰器是为了对函数的执行前后操作而使用存在，但是又不改动原来的函数
@Date       :2024/04/13 15:29:36
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
# 装饰器函数,会把原始函数名传入其中


def outer(func):
    print("把原始函数传入装饰器函数中...")
    print(func)

    def inner(param):
        print("origin_func之前的操作")
        ret = func(param)
        print("origin_func之后的操作")
        return ret
    return inner


@outer
def origin_func(param):  # 原始函数
    return "hello,"+param


str = origin_func("daito")  # 此时执行的已经是被装饰后的函数，inner()
print(str)
