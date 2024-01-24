'''
@FileName   :auth.py
@Description:登录页
@Date       :2023/12/09 09:51:12
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from flask import Blueprint

bp = Blueprint("auth", __name__, url_prefix="/auth")

# @app.route("/")不再是flask-app了,而是子集blueprint--bp


@bp.route("/login")
def login():
    pass
