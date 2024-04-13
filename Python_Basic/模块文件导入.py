'''
@FileName   :模块文件导入.py
@Description:需要注意的导入时的目录树，避免导入出错
@Date       :2024/04/13 16:13:00
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import sys
from dictory import 类01, 类02
'''
导入时，优先同级目录，其次是上一级的包，最后是环境下的包
'''
print(sys.path)
pp = 类02.p1
print(pp)
