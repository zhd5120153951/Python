'''
@FileName   :class05.py
@Description:
@Date       :2022/05/19 10:57:57
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''


class Enemy:
    # __方法名__表示这是系统内置函数且该类函数为纯虚函数(Python中纯虚函数为可重写函数)
    def __init__(self, name, hp, atk, defense) -> None:
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense

    def __str__(self) -> str:  # 箭头表示的函数返回类型——符合用户逻辑的可重写函数
        return "敌人%s目前剩余血量%d且攻击力是%d防御力是%d" % (self.name, self.hp, self.atk, self.defense)

    def __move__(self):
        print(self.name + "打不过，我先溜了")

    # def __repr__(self) -> str:符合解释器语法逻辑的可重写函数
    #     pass


class USA(Enemy):
    def __init__(self, name, hp, atk, defense) -> None:
        super().__init__(name, hp, atk, defense)

    def __str__(self) -> str:
        return "敌人%s——目前剩余血量%d——且攻击力是%d——防御力是%d" % (self.name, self.hp, self.atk, self.defense)

    def __move__(self):  # 以上三个函数都是重写
        print(self.name + "打不过，我先溜了")


e = Enemy("疾风剑豪", 100, 120, 90)
print(e.__str__())
e.__move__()
u = USA("米国佬", 10, 5, 0)
print(u.__str__())
u.__move__()
