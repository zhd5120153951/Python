'''
@FileName   :class04.py
@Description:
@Date       :2022/05/16 11:17:23
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''


class Graphics:  # 相当于C++中的抽象类
    def __init__(self) -> None:  # 相当于纯虚函数
        pass

    def Area(self):  # 只声明，不定义——相当于纯虚函数
        pass


class Circle(Graphics):
    def __init__(self, radius) -> None:  # 必须重写纯虚函数（联想C++的继承多态性质）
        self.radius = radius

    def Area(self):
        return 3.14 * self.radius * self.radius


class Rectangle(Graphics):
    def __init__(self, width, height):
        self.width = width
        self.height = height  # python中默认成员为公有

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    def Area(self):
        return self.width * self.height


c = Circle(10)
print(c.Area())
r = Rectangle(20, 10)
print(r.__dict__)
print(r.Area())
r.width = int(input("请输入宽："))
print(r.Area())
