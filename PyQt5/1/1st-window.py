'''
@FileName   :1st-window.py
@Description:
@Date       :2023/11/14 10:04:47
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''

from PyQt5.Qt import *
from PyQt5.QtGui import QIcon
import sys

# 创建应用程序对象
app = QApplication(sys.argv)
# 实例化一个QWidget对象
window = QWidget()
# 设置window标题
window.setWindowTitle("1st-window")
# 设置window对象的大小
window.resize(980, 500)
# 设置window对象的ico图标
window.setWindowIcon(QIcon("D:\\Zengh\\Pictures\\opencv.ico"))

# 实例化一个按钮对象，并使其继承与window对象
btn = QPushButton(window)
# 设置btn按钮对象的文本
btn.setText('确定')
# 设置btn按钮对象的大小
btn.resize(135, 95)
# 设置btn按钮对象左上角距离window对象左上角的距离
btn.move(200, 100)

# 显示窗体
window.show()

# sys.exit 检测退出原因，正常退出为0，非正常退出为1
# app.exec_() 消息循环功能
sys.exit(app.exec_())
