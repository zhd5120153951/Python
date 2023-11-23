'''
@FileName   :app.py
@Description:这个是python写的后端代码--处理的是前端的响应--整个框架使用flask
@Date       :2023/11/15 10:29:58
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
from calendar import c
# from crypt import methods  # 这个crypt包不支持Windows
from flask import Flask, redirect, render_template, Response, request, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
# from django.shortcuts import render,redirect #django是复杂的部署前后端框架---flask是轻量型的,快速部署的框架
import logging
import cv2
import psutil
import sqlite3
import functions

# 配置基本日志设置
logging.basicConfig(
    level=logging.DEBUG,  # 设置日志级别，可以选择DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志消息的格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期时间格式
    filename='./App.log',  # 指定日志输出到文件
    filemode='w'  # 指定文件写入模式（a表示追加，w表示覆盖）
)

# 创建一个日志记录器
logger = logging.getLogger('my_logger')

# 创建网页应用对象
app = Flask(__name__)  # 这里是默认html文件的目录是：templates
# app = Flask(__name__, 'html_dir')
# 配置数据库文件路径
DATABASE = 'user_database.db'

# 使用OpenCV捕获RTSP流
rtsp_url = "rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101"
cap = cv2.VideoCapture(rtsp_url)
# 用户默认信息
users = {'admin': 'password'}


# 创建数据库表
def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            );
        ''')


# 首页--默认login


@app.route('/')
def default_page():
    return redirect('/login')


# 注册


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username,password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


# 登陆接口--登陆成功跳转管理页面homepage,否则提示账号没有注册(或者注册了提示密码出错)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        res = functions.login()
        if res == 1:
            return redirect('/index')
        else:
            return res
    # if request.method == 'POST':  # 用户发起求登录请求
    #     username = request.form['username']
    #     password = request.form['password']
    #     logger.info(username)
    #     logger.info(password)
    #     with sqlite3.connect(DATABASE) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             'SELECT * FROM users WHERE username = ?', (username, ))
    #         user = cursor.fetchone()

    #     if user and check_password_hash(user[2], password):
    #         logger.info("success")
    #         # return '登陆成功'  # 这个应该就跳转到成功后界面
    #         # return render_template('homepage.html')
    #         return redirect(url_for('homepage'))
    #     # else:
    #         # return '登陆失败,请检查用户名和密码'
    # return render_template('login.html')


# 主页

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")  # 返回的是一个html页面,其实还可以返回文字等信息


# 路由：获取 CPU 使用率的 API


@app.route('/get_resources')
def get_cpu_usage_api():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory().percent
    disk_info = psutil.disk_usage('/').percent
    gpu_info = "Not Implemented"  # 这个可能需要其他的包来获取GPU信息
    logger.info(cpu_usage)

    data = {
        'cpu': cpu_usage,
        'memory': memory_info,
        'disk': disk_info,
        'gpu': gpu_info
    }

    print(data)
    return jsonify(data)


# 登陆页面--需要和后端交互的--['GET','POST']


@app.route('/login_1', methods=['GET', 'POST'])
def login_1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # 登陆成功,重定向到首页
            return redirect(url_for('homepage'))

    # 渲染信息页面
    return render_template('login_1.html')


# 设备信息页面


@app.route('/device')
def devices():
    return render_template("device.html")

# 关于页面


@app.route('/about')
def about():
    return render_template('about.html')


# 获取视频每帧--3


def generate_frames():
    logger.info("generate_frames execute...")
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 路由函数--点击后的新页面--执行顺序1


@app.route('/web_rtsp')
def web_rtsp():
    logger.info("web_rtsp execute...")
    return render_template('web_rtsp.html')

# 路由函数--网页显示每帧视频--2


@app.route('/video_feed')
def video_feed():
    logger.info("video_feed execute...")
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":

    create_table()
    # 配置密钥,用于加密session数据
    app.config['SECREAT_KEY'] = 'daito_yolov5_flask'
    app.run(host="0.0.0.0", debug=True)
