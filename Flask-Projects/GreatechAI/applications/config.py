import logging
from datetime import timedelta


class BaseConfig:
    SUPERADMIN = 'admin'
    SYSTEM_NAME = 'GreatchAI'
    # 主题面板的链接列表配置
    SYSTEM_PANEL_LINKS = [
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "官方网站",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开发文档",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开源地址",
            "href": "https://gitee.com/Jmysy/Pear-Admin-Layui"
        }
    ]
    UPLOADED_PHOTOS_DEST = 'static/upload'
    UPLOADED_FILES_ALLOW = ['gif', 'jpg', 'png', 'icon']
    UPLOADS_AUTOSERVE = True
    # Json配置
    JSON_AS_ASCII = False
    # 密钥配置
    SECRET_KEY = 'greatech-system-flask'
    # 数据库配置
    # MySQL
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'ZHDzhd2231'
    MYSQL_HOSTNAME = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'GreatechAI'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

    # Sqlite配置
    # SQLALCHEMY_DATABASE_URI = "sqlite:///../greatech.db"

    # 配置多个数据库连接的连接串写法示例
    # HOSTNAME: 指数据库的IP地址、USERNAME：指数据库登录的用户名、PASSWORD：指数据库登录密码、PORT：指数据库开放的端口、DATABASE：指需要连接的数据库名称
    # MSSQL: f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=cp936"

    # MySQL: f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

    # Oracle: f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"

    # Oracle的第二种连接方式
    # dsnStr = cx_Oracle.makedsn({HOSTNAME}, 1521, service_name='orcl')
    # connect_str = "oracle://%s:%s@%s" % ('{USERNAME}', ' {PASSWORD}', dsnStr)

    # SQLite: "sqlite:/// database.db"

    # Postgres: f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"

    #  在SQLALCHEMY_BINDS 中设置：'{数据库连接别名}': '{连接串}'
    # 最后在models的数据模型class中，在__tablename__前设置        __bind_key__ = '{数据库连接别名}'  即可，表示该数据模型不使用默认的数据库连接，改用“SQLALCHEMY_BINDS”中设置的其他数据库连接
    #  SQLALCHEMY_BINDS = {
    #  'testMySQL': 'mysql+pymysql://test:123456@192.168.1.1:3306/test?charset=utf8',
    #  'testMsSQL': 'mssql+pymssql://test:123456@192.168.1.1:1433/test?charset=cp936',
    #   'testOracle': 'oracle+cx_oracle://test:123456@192.168.1.1:1521/test',
    #   'testSQLite': 'sqlite:///database.db
    # }

    # 默认日志等级
    LOG_LEVEL = logging.WARN
    # 邮箱配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USERNAME = '2462491568@qq.com'
    MAIL_PASSWORD = 'XXXXX'  # 腾讯QQ邮箱网页上生成
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # 插件配置,填写插件的文件名称,默认不开启插件
    PLUGIN_ENABLE_FOLDERS = []
    # session
    PERMANENT_SESSION_LEFTTIME = timedelta(days=7)
    SESSION_TYPE = 'filesystem'  # 默认使用文件系统来保存会话
    SESSION_PERMANENT = False  # 会话是否持久化
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上的session中的cookie值进行加密
