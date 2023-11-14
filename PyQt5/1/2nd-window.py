'''
@FileName   :2nd-window.py
@Description:
@Date       :2023/11/14 10:22:06
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

# 创建一个应用程序对象
# sys.argv：用于接收用户在命令行启动该程序时传递过来的参数
app = QApplication(sys.argv)
# 实例化一个QWidget对象
window = QWidget()
# 设置window对象的标题
window.setWindowTitle('2nd-window')
# 设置window对象的大小
window.resize(980, 500)
# 设置window对象的ico图标
window.setWindowIcon(QIcon('D:\\Zengh\\Pictures\\opencv.ico'))

# 实例化一个按钮对象，并使其继承与window对象
btn = QPushButton(window)
# 设置btn按钮对象的文本
btn.setText('确定')
# 设置btn按钮对象的大小
btn.resize(135, 95)
# 设置btn按钮对象左上角距离window对象左上角的距离
btn.move(200, 100)

# 实例化一个标签对象，并未继承于window对象
lab_2 = QLabel()
# 设置标签对象的窗体标题
lab_2.setWindowTitle('标签')
# 设置标签对象显示的文本
lab_2.setText('取消')
# 设置标签对象的大小
lab_2.resize(300, 200)

# 显示窗体
window.show()
lab_2.show()

# sys.exit 检测退出原因，正常退出为0，非正常退出为1
# app.exec_() 消息循环功能
sys.exit(app.exec_())
