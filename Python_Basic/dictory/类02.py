'''
@FileName   :Game.py
@Description:
@Date       :2022/05/13 12:12:14
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''


class Person:
    '''
    实例方法
    默认公有实例变量——加了property后就变为私有实例变量
    '''
    def __init__(self, name, age, score):  # 没有init()则表示没有构造函数，实例化对象时可以不加()
        self.name = name
        self.age = age
        self.score = score

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, age):
        self.__age = age

    def Go_to(self, dest, type):
        type.run(dest)


class Car:
    """汽车类——没有构造函数init()"""
    def run(dest):
        print("张无忌开车去", dest)


p1 = Person("恶龙咆哮", 1200, 100)
print(p1.name, p1.age)
print(p1.__dict__)
p1.name = "张无忌"
p1.age = 24
p1.score = 150  # 公有实例变量(因为没有加property)
print(p1.name, p1.age)
print(p1.__dict__)
c1 = Car
p1.Go_to("北京", c1)
