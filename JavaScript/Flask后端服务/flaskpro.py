'''
@FileName   :flaskpro.py
@Description:
@Date       :2024/01/12 15:23:11
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from flask import Flask
import flask_cors

app = Flask(__name__)


# 后端接口--路由
@app.route('/')
def index():
    return "hello world"


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)
