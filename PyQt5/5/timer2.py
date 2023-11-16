from PyQt5.Qt import *
import sys


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QObject定时器")
        self.resize(200, 200)
        self.w = self.width()
        self.h = self.height()

    def timerEvent(self, a0: "QTimerEvent"):
        self.resize(self.width()+10, self.height()+10)
        if self.width() == 2*self.w and self.height() == 2*self.h:
            print(f"{self.width()}__{self.height()}")
            self.killTimer(self.timer_id)

    def mystartTimer(self, ms):
        self.timer_id = self.startTimer(ms)


app = QApplication(sys.argv)
w = MyWidget()
print(f"{w.width()}__{w.height()}")

w.mystartTimer(100)
w.show()
sys.exit(app.exec_())
