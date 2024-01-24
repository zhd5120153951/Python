'''
@FileName   :qa.py
@Description:问答首页
@Date       :2023/12/09 09:50:52
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from flask import Blueprint

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    pass
