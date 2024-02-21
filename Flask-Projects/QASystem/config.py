'''
@FileName   :config.py
@Description:系统配置
@Date       :2024/02/05 16:18:13
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
import os

# 数据库配置
HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'qa'
USERNAME = 'root'
PASSWORD = 'ZHDzhd2231'
DB_URI = 'mysql+mysqldb://{}:{}@{}:{}/{}'.format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

# 邮箱配置信息
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "2462491568@qq.com"
MAIL_PASSWORD = "axsakjxrdgiseaha"  # 授权码唯一的(网页上获取),flask登陆邮箱的必须--可能因过期导致无法发送
MAIL_DEFAULT_SENDER = "2462491568@qq.com"

SECRET_KEY = os.urandom(24)

SECRET_KE = "fafadgrawewga"
