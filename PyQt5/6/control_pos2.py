import sys
from PyQt5.Qt import *

app = QApplication(sys.argv)
window = QWidget()
window.resize(500, 500)

window.show()

# 总的控件个数
widget_count = 20
# 一行有多少个控件（列）
column_count = 3
# 总行数
row_count = (widget_count - 1) // column_count + 1

# 一个控件的宽度(要求是个integer整数类型）
widget_width = int(window.width() / column_count)
#  一个控件的高度(要求是个integer整数类型）
widget_height = int(window.height() / row_count)

for i in range(0, widget_count):
    win = QWidget(window)
    win.resize(widget_width, widget_height)
    # 通过控件所在列号*控件宽度，算出x位置（列号是从0开始）
    win_pos_x = i % column_count * widget_width
    # 通过控件所在行号*控件高度，算出y位置（行号是从0开始）
    win_pos_y = i // column_count * widget_height
    win.move(win_pos_x, win_pos_y)
    win.setStyleSheet('background-color:red;border: 1px solid yellow;')
    win.show()

sys.exit(app.exec_())
