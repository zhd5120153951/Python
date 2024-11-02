'''
@FileName   :反射特性.py
@Description:
@Date       :2024/11/02 10:21:29
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
@PS         :
'''

import cv2


# 类
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}."

    def celebrate_birthday(self):
        self.age += 1
        return f"I'm now {self.age} years old!"


# 反射示例
def main():
    # 创建 Person 对象
    person = Person("Alice", 30)

    # 使用反射访问属性--直接返回属性值
    name_attr = getattr(person, 'name')
    age_attr = getattr(person, 'age')
    # gender_attr = getattr(person, 'gender')
    print(f"Name: {name_attr}, Age: {age_attr}")
    # print(f"Gender:{gender_attr}")  # 会报错
    # 使用反射修改属性
    setattr(person, 'name', 'Bob')
    setattr(person, 'age', 31)
    print(f"Updated Name: {person.name}, Updated Age: {person.age}")

    # 使用反射调用方法--返回方法的地址--函数名，需要加()才能执行
    greet_message = getattr(person, 'greet')()
    print(greet_message)

    birthday_message = getattr(person, 'celebrate_birthday')()
    print(birthday_message)


# 入口
if __name__ == "__main__":
    main()
    cap = cv2.VideoCapture(
        "rtsp://admin:@ZHDzhd2231@192.168.10.250:554/Streaming/Channels/101")
    if cap.isOpened():
        print("cap is opened....")
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("1.jpg", frame)
        else:
            print("解码出错........")
