'''
@FileName   :app.py
@Description:
@Date       :2023/12/08 21:38:34
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
# 本地包
from extension import db
from models import UserModel

from blueprints.auth import bp as auth_bp
from blueprints.qa import bp as qa_bp

import config
# 第三方包
from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
# app绑定到数据库对象
db.init_app(app)

migrate = Migrate(app, db)

# app和bp注册关联--主子关系
app.register_blueprint(auth_bp)
app.register_blueprint(qa_bp)

# blueprints用来模块化html的,相当于flask的一个子集


if __name__ == "__main__":
    app.run()
