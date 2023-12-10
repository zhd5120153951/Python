from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from matplotlib.backend_bases import cursors
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import logging
import cv2
import psutil
from sympy import threaded, true

# 创建网页应用对象
app = Flask(__name__)
# app.config["secret_key"] = 'daito_yolov5_flask'

# 配置密钥,用于加密session数据
# app.config['SECREAT_KEY'] = "daito_yolov5_flask"
app.secret_key = "daito_yolov5_flask"
# app.secret_key = 'kdjklfjkd87384hjdhjh'

# 初始化 Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


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
    user = User(id='123')  # 举例，创建一个用户
    login_user(user)  # 通过 Flask-Login 登录用户
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username, ))
        isExistUser = cursor.fetchone()

    if isExistUser and check_password_hash(isExistUser[2], password):
        flash('Login successful', 'message')
        return redirect(url_for('homepage'))  # redirect()是某个页面的路由函数

    # if isExistUser:
    #     flash('Login successful', 'success')
    #     return redirect(url_for('homepage'))  # redirect()是某个页面的路由函数

    # else:
    #     flash('Invalid username or password', 'error')
    #     return redirect(url_for('home'))
    flash('Invalid username or password', 'info')
    return redirect(url_for('home'))
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
@login_required  # 应用到受保护的页面
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
@login_required  # 应用到受保护的页面
def web_rtsp():
    return render_template('web_rtsp.html')

# 路由--获取rtsp视频


@app.route('/video_feed')
@login_required  # 应用到受保护的页面
def video_feed():
    isVideo = True
    return Response(generate_frames(isVideo), mimetype='multipart/x-mixed-replace; boundary=frame')

# 路由：获取 CPU 使用率的 API--由jquery发起


@app.route('/get_resources')
@login_required  # 应用到受保护的页面
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
# 路由--跳转到portip


@app.route('/portip', methods=['GET', 'POST'])
@login_required  # 应用到受保护的页面
def portip():
    return render_template('portip.html')

# 路由--改ip


@app.route('/set_ip')
@login_required  # 应用到受保护的页面
def set_ip():
    pass

# 路由--ip_config


@app.route('/ip_config')
@login_required  # 应用到受保护的页面
def ip_config():
    return render_template("ip_config.html")
# 路由--rtsp_config


@app.route('/rtsp_config')
def rtsp_config():
    pass
# 路由--system_resource


@app.route('/system_resource')
def system_resource():
    pass

# 路由--rtsp_config


@app.route('/ai_setting')
def ai_setting():
    pass


# 哑用户类


class User(UserMixin):
    def __init__(self, id):
        self.id = id

# 用户加载函数，传入用户 ID，返回用户对象


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


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

    # Flask-Login 需要一个自定义的消息和重定向端点
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "login"

    create_table()

    app.run(host="0.0.0.0", debug=True)
    # app.run(host="0.0.0.0", debug=True)
