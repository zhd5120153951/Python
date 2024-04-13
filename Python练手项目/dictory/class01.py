str = "  hdjsdb  defdje 都的剥削 毒性创新    成都 汉州    "
print(str)
str1 = str.rstrip().lstrip()
print(str1)
str2 = str1.replace(" ", "")
print(str2)
tp = (x * x for x in range(1, 10, 1))
print(*tp)
tp1 = (x * x for x in range(1, 10, 1) if x % 2 != 0)
print(*tp1)


class Person:
    # 这是实例方法——这是在建立类对象时才使用
    def __init__(self, name, age, score, gender):  # 这是实例变量
        self.name = name
        self.age = age
        self.score = score
        self.gender = gender

    # 这也是实例方法
    def say_hi(self):
        print("Hello, my name is", self.name, self.age, self.score, self.gender)

    # 这是类变量——一般用于共享数据会使用
    name = ""
    age = 0
    score = 0
    # 这是类方法——共享方法会使用

    @classmethod
    def __initial__(cls):
        cls.name = "三丰"
        cls.age = 100
        cls.score = 150


Person.__initial__()
print(Person.name)
print(Person.age)
print(Person.score)
l1 = []
while True:
    name = input("输入名字：")
    age = int(input("输入年龄："))
    score = int(input("输入成绩："))
    gender = input("输入性别：")
    l1.append(name)
    l1.append(age)
    l1.append(score)
    l1.append(gender)
    break

p = Person(*l1)
p.say_hi()
p.name = "张无忌"
p.score = 150
p.age = 24
p.gender = "女"
p.say_hi()
# The previous 2 lines can also be written as
# Person('Swaroop').say_hi()
