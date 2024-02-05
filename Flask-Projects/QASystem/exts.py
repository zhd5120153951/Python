'''
@FileName   :exts.py
@Description:这个文件存在的意义就是为了解决循环引用
@Date       :2024/02/05 16:21:09
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()  # 实例化数据库对象
mail = Mail()  # 实例化邮箱对象
