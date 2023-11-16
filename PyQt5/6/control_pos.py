import sys
from PyQt5.Qt import *

app = QApplication(sys.argv)
w1 = QWidget()
# 设置用户区域大小--交互区域
w1.setGeometry(300, 300, 500, 500)
w1.setWindowTitle("w1")

w2 = QWidget()
w2.resize(500, 500)
# 设置窗体的位置和大小,包含框架
w2.move(300, 300)
w2.setWindowTitle("w2")

w1.show()
w2.show()

sys.exit(app.exec_())
