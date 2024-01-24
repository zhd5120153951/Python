'''
@FileName   :config.py
@Description:专门存放配置文件
@Date       :2023/12/08 21:38:22
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''

HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "qa"
USERNAME = "root"
PASSWORD = "ZHDzhd2231"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
# DB_URI = "mysql+pymysql://root:@ZHDzhd2231@127.0.0.1:3306/qa?charset=utf8"
SQLALCHEMY_DATABASE_URI = DB_URI
