from PyQt5.Qt import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(500, 500)
    window.setWindowTitle("自定义鼠标样式")

    # 创建QPixmap对象，并设置显示的图片
pixmap = QPixmap("./PyQt5/7/image-1.png")

# 设置对象宽和高按比例缩小，返回一个新对象
new_pixmap = pixmap.scaled(20, 20)

# 创建QCursor对象(鼠标对象)，用作setCursor参数
# 设置该对象的作用点为图片的左上角(0,0)，默认是图片中心点
cursor = QCursor(new_pixmap, 0, 0)

# 设置window控件的鼠标样式为自定义的QCursor对象：cursor
window.setCursor(cursor)

window.show()
sys.exit(app.exec_())
