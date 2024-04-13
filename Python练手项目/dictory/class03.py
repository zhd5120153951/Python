'''
@FileName   :class03.py
@Description:
@Date       :2022/05/15 10:51:59
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''


class Person:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def say(self):
        print("我是人类")


class Student(Person):
    def __init__(self, name, age, score) -> None:
        super().__init__(name, age)  # python中子类构造一定调用父类构造
        self.score = score

    def smile(self):
        print("学生笑了")


class Teacher(Person):
    def __init__(self, name, age, salary) -> None:
        super().__init__(name, age)
        self.salary = salary

    def play(self):
        print("老师玩了")


p = Person("张无忌", 24)
print(p.name, p.age)
# print(p.score) 父类不能调用子类实例变量，实例方法
s = Student("张三", 20, 60)
print(s.name, s.age, s.score)
s.say()
s.smile()
t = Teacher("张三丰", 150, 10000)
print(t.name, t.age, t.salary)
t.say()
t.play()
