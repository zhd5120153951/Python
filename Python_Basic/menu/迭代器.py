'''
@FileName   :class07.py
@Description:迭代器的本质——对可迭代对象，返回一个迭代器对象
@Date       :2022/05/24 10:26:42
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''

# 可迭代类


class IterableObject():
    def __init__(self) -> None:
        pass

    def __iter__(self):
        return IteratorObject()

# 迭代器类


class IteratorObject():
    def __init__(self, target, index) -> None:
        self.__target = target
        self.__index = index

    def __next(self):
        if self.__index > len(self.__target) - 1:
            raise
        temp = self.__target[self.__index]
        self.__index += 1
        return temp
