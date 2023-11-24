from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
import sqlite3
import logging
import cv2
import psutil


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
app = Flask(__name__)
app.secret_key = '@ZHDzhd2231'
# 使用OpenCV捕获RTSP流
rtsp_url = "rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101"
cap = cv2.VideoCapture(rtsp_url)

# Function to connect to the SQLite database


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

# 路由--first page


@app.route('/')
def home():
    return render_template('login.html')

# 路由--login page


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    connection = get_db_connection()
    isExistUser = connection.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    connection.close()

    if isExistUser:
        flash('Login successful', 'success')
        return redirect(url_for('homepage'))  # redirect()是某个页面的路由函数

    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('home'))

# Route for the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        connection = get_db_connection()
        connection.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        connection.commit()
        connection.close()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


# 获取视频每帧--3


def generate_frames():
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
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
# 路由--跳转到portip


@app.route('/portip', methods=['GET', 'POST'])
def portip():
    return render_template('portip.html')

# 路由--改ip


@app.route('/set_ip')
def set_ip():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
    # app.run(host="0.0.0.0", debug=True)
