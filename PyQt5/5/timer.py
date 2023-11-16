from PyQt5.Qt import *
import sys

from cv2 import resize


class MyLabel(QLabel):
    def timerEvent(self, a0: 'QTimerEvent'):
        initial_ms = int(self.text())
        initial_ms -= 1
        if initial_ms >= 0:
            self.setText(str(initial_ms))


app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('QObject定时器')
w.resize(600, 600)

label = MyLabel(w)
label.resize(w.width(), w.height())
label.setText("10")
label.setStyleSheet("font-size:180px;color:red;")
label.setAlignment(Qt.AlignCenter)

label.startTimer(1000)
w.show()
sys.exit(app.exec_())
