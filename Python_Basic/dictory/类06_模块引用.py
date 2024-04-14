'''
@FileName   :class06.py
@Description:python核心知识——散点
@Date       :2022/05/22 10:20:24
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from Python_Basic.dictory.类01_封装 import Person
import Python_Basic.dictory.类02_变量封装 as 类02_变量封装
import Python_Basic.dictory.类04_继承 as cl04
from Python_Basic.dictory.类05_多态 import Enemy, USA
from Python_Basic.dictory.类05_多态 import *

cir = cl04.Circle(12)
c = 类02_变量封装.Car()

p = Person("死亡", 123, 12, "男")
print(p.name, p.age, p.score, p.gender)
