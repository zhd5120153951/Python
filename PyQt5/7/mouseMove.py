from PyQt5.Qt import *
import sys


class MyWidget(QWidget):
    def mouseMoveEvent(self, ms) -> None:

        # 获取指定类型，指定对象名称的子控件
        label = self.findChild(QLabel, 'label2')
        # 设置label的位置方法一
        # ms_pos = ms.pos()
        # label.move(ms_pos)
        ms_pos = ms.localPos()
        label.move(int(ms_pos.x()), int(ms_pos.y()))


app = QApplication(sys.argv)
window = MyWidget()
window.resize(500, 500)
window.setWindowTitle("鼠标跟踪案例")

# 设置鼠标样式为指定图片
pixmap = QPixmap('/PyQt5/7/image.png')
new_pixmap = pixmap.scaled(20, 20)
cursor = QCursor(new_pixmap, 0, 0)
window.setCursor(cursor)

# 窗口添加label标签控件
label1 = QLabel(window)
label1.setObjectName('label1')
label1.setText('鼠标跟踪案例1')
label1.move(100, 100)
label1.setStyleSheet("background-color:cyan;")

label2 = QLabel(window)
label2.setObjectName('label2')
label2.setText('鼠标跟踪案例2')
label2.move(200, 200)
label2.setStyleSheet("background-color:red;")


# 设置窗口开启鼠标跟踪
window.setMouseTracking(True)


window.show()
sys.exit(app.exec_())
