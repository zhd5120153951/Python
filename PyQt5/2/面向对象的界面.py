from PyQt5.Qt import *
import sys


class Window(QWidget):  # 继承方式
    # 重写父类构造
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("面向对象的窗体")
        self.resize(500, 500)
    # 添加子控件

    def setup_ui(self):
        label = QLabel(self)
        label.setText("点击...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.setup_ui()
    window.show()
    sys.exit(app.exec_())
