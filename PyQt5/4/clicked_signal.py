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

    def btn_slot(self):
        print('clicked me what ')
        self.setWindowTitle("clicked modify title")

    def add_widget(self):
        btn = QPushButton(self)
        btn.setText("click me")
        btn.clicked.connect(self.btn_slot)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Windows()

    w.show()
    sys.exit(app.exec_())
