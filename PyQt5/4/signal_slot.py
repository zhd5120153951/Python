from PyQt5.Qt import *
import sys


class Windows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('')
        self.resize(980, 500)
        self.widget_list()

    def widget_list(self):
        self.add_widget()

    def windowtitle_slot(self, title):
        # 临时取消信号与槽的连接，防止下面修改标题进入死循环
        self.blockSignals(True)
        self.setWindowTitle('新标题 - ' + title)
        # 恢复信号与槽的连接，为下一次修改标题做准备
        self.blockSignals(False)

    def add_widget(self):
        self.windowTitleChanged.connect(self.windowtitle_slot)
        self.setWindowTitle('Hello')
        self.setWindowTitle('World')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Windows()

    w.show()
    sys.exit(app.exec_())
