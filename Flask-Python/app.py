from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from matplotlib.backend_bases import cursors
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import logging
import cv2
import psutil
from ipaddress import ip_address, AddressValueError
import netifaces
import socket
from sympy import threaded, true

# 创建网页应用对象
app = Flask(__name__)
# app.config["secret_key"] = 'daito_yolov5_flask'

# 配置密钥,用于加密session数据
# app.config['SECREAT_KEY'] = "daito_yolov5_flask"
app.secret_key = "daito_yolov5_flask"
# app.secret_key = 'kdjklfjkd87384hjdhjh'


def get_db_connection():
    connection = sqlite3.connect('users.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to initialize the database


def init_db():
    with app.app_context():
        connection = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            connection.cursor().executescript(f.read())
        connection.commit()
        connection.close()

# 创建数据库表


def create_table():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            );''')

# 路由--first page


@app.route('/')
def home():
    # init_db()
    return render_template("login.html")

# 路由--login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM users WHERE username = ?', (username, ))
            isExistUser = cursor.fetchone()

        if isExistUser and check_password_hash(isExistUser[2], password):
            flash('Login successful', 'success')
            return redirect(url_for('homepage'))  # redirect()是某个页面的路由函数

        flash('Invalid username or password', 'info')
        return redirect(url_for('/'))
    else:
        return render_template("login.html")
# 注销用户


@app.route('/logout')
def logout():
    logout_user()  # 通过 Flask-Login 注销用户
    return redirect(url_for('home'))
# Route for the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(password)
        hashed_password = generate_password_hash(password)
        print(hashed_password)
        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username,password) VALUES (?,?)", (
                    username, hashed_password)
            )
            conn.commit()
        flash('Registration successful. You can now log in.', 'message')
        return redirect(url_for('home'))
    flash('Registration failure. try again.', 'info')
    return render_template('register.html')


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


# 获取视频每帧


def generate_frames(isVideo):
    if isVideo:
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# 路由--跳转web_rtsp


@app.route('/web_rtsp', methods=['GET', 'POST'])
def web_rtsp():
    return render_template('web_rtsp.html')

# 路由--获取rtsp视频


@app.route('/video_feed')
def video_feed():
    isVideo = True
    return Response(generate_frames(isVideo), mimetype='multipart/x-mixed-replace; boundary=frame')

# 路由：获取 CPU 使用率的 API--由jquery发起


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

# 获取IP


def get_ip_addr():
    ip_addr = {"local_ip": "", "wifi_ip": ""}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(s)
    # 尝试连接非存在地址，来激活网络接口的 IP
    try:
        # 这里的地址不需要真实存在
        s.connect(("10.255.255.255", 1))
        ip_addr['local_ip'] = s.getsockname()[0]

        print(ip_addr['local_ip'])
        print(s.getsockname()[1])

    except:
        ip_addr['local_ip'] = 'N/A'
    # 获取 WiFi IP 地址（这种方式较为复杂，可能需要根据具体操作系统及网络配置而定）
    # 这里我们假装已经得到了 WiFi IP 地址
    ip_addr['wifi_ip'] = '192.168.0.10'
    s.close()
    return ip_addr
# 路由--ip_config


@app.route('/ip_config', methods=['GET', 'POST'])
def ip_config():
    ip_addr = get_ip_addr()
    return render_template("ip_config.html", ip_addr=ip_addr)
    # # 显示当前的端口或者WiFi ip地址
    # try:
    #     # 获取本地网络接口列表
    #     interfaces = [ip_address(i) for i in netifaces.interfaces()]
    #     # 获取本地ip
    #     local_ip = interfaces[0].ip
    #     # 获取WiFi IP地址
    #     wifi_ip = None
    #     for i in interfaces:
    #         if i.is_wireless:
    #             wifi_ip = i.ip
    #             break
    #     # 渲染模板
    #     return render_template("ip_config.html", local_ip, wifi_ip)

    # except AddressValueError as e:
    #     return f"Error:{e}"


# 设置IP--Port(WiFi一般都是自动分配IP,不需要设置)
def set_ip_addr(interface="eth0", new_ip=None):
    if new_ip:
        try:
            netifaces.ifaddresses(interface)[
                netifaces.AF_INET][0]['addr'] = new_ip
            return True
        except KeyError:
            return False
    else:
        return False

# 路由--改ip


@app.route('/set_ip', methods=['GET', 'POST'])
def set_ip():
    if request.method == "POST":
        new_ip = request.form.get('new_ip')
        interface = "eth0"
        print(new_ip)
        if set_ip_addr(interface, new_ip):
            return redirect(url_for("ip_config"))
        else:
            return "IP设置失败"
# 路由--rtsp_config


@app.route('/rtsp_config')
def rtsp_config():
    # 获取当前的摄像头rtsp
    return render_template("rtsp_config.html")


@app.route('/set_rtsp')
def set_rtsp():
    return "rtsp设置成功"

# 路由--system_resource


@app.route('/system_resource')
def system_resource():
    return "system_resource 成功"

# 路由--rtsp_config


@app.route('/ai_setting')
def ai_setting():
    return "AI设置成功"


if __name__ == '__main__':
    # 配置基本日志设置
    logging.basicConfig(
        level=logging.DEBUG,  # 设置日志级别，可以选择DEBUG, INFO, WARNING, ERROR, CRITICAL
        # 设置日志消息的格式
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期时间格式
        filename='./App.log',  # 指定日志输出到文件
        filemode='w'  # 指定文件写入模式（a表示追加，w表示覆盖）
    )
    # 创建一个日志记录器
    logger = logging.getLogger('my_logger')

    # 使用OpenCV捕获RTSP流
    # rtsp_url = "rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101"
    rtsp_url = 0
    cap = cv2.VideoCapture(rtsp_url)

    create_table()

    app.run(host="0.0.0.0", debug=True)
    # app.run(host="0.0.0.0", debug=True)
