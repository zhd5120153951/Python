from flask import Flask, Blueprint


# 创建sys--系统蓝图
system_bp = Blueprint('system', __name__, url_prefix='/system')


def register_system_bps(app: Flask):
    app.register_blueprint(system_bp)
