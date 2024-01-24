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
from flask import Flask, request
from flask_cors import cross_origin


app = Flask(__name__)


# 后端接口--路由
@app.route('/')
@cross_origin()  # 跨域问题
def index():
    return "hello world"
# flask中路由默认get请求,所以需要怎么访问,要加methods


@app.route('/get/', methods=["GET", "POST"])
@cross_origin()
def get():
    # request.args:专门用来接收前端传来的GET参数
    print(request.args)
    d = {"name": "daito", "age": 28}
    return d


@app.route('/post/', methods=["GET", "POST"])
@cross_origin()
def post():
    # request.form用来接收前端的POST参数:表单等
    print(request.form)
    print(request.form['username'])
    print(request.form['password'])
    d = {"name": "adog", "age": 12}
    return d  # 返回给前端的


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, True)
