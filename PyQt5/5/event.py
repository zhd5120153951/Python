import sys
from PyQt5.Qt import *


class QApp(QApplication):
    def notify(self, receiver, evt):
        if receiver.inherits('QPushButton') and evt.type() == QEvent.MouseButtonPress:
            print('QApp对象里面的notify方法', receiver, evt)

        return super().notify(receiver, evt)


class Btn(QPushButton):
    def event(self, evt):
        if evt.type() == QEvent.MouseButtonPress:
            print('Btn中的event方法', evt)
        return super().event(evt)

    def mousePressEvent(self, evt):
        print('Btn中的MouseButtonPress方法', evt)
        return super().mousePressEvent(evt)


app = QApp(sys.argv)

window = QWidget()

btn1 = Btn(window)
btn1.setText('登录')
btn1.move(100, 100)

# 这种方式最好,不要再次封装QPushButton类
btn2 = QPushButton(window)
btn2.setText('取消')
btn2.move(100, 150)


def cao1():
    print(f'用户按下了【登录】按钮—信号与槽机制')


def cao2():
    print(f'用户按下了【取消】按钮—信号与槽机制')


btn1.pressed.connect(cao1)
btn2.pressed.connect(cao2)

window.show()
sys.exit(app.exec_())
