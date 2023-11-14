from calendar import c
from flask import Flask, redirect, render_template, Response, request, url_for, jsonify
import logging
import pkgutil
import time
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
app = Flask(__name__)  # 这里是默认html文件的目录是：templates
# app = Flask(__name__, 'html_dir')

# 使用OpenCV捕获RTSP流
rtsp_url = "rtsp://admin:jiankong123@192.168.23.10:554/Streaming/Channels/101"
cap = cv2.VideoCapture(rtsp_url)
# 用户默认信息
users = {'admin': 'password'}


# 首页--静态页面
@app.route('/')
def index():
    return render_template("index.html")


# 获取CPU使用率


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)  # 1秒获取一次

# 路由：获取 CPU 使用率的 API


@app.route('/get_cpu_usage')
def get_cpu_usage_api():
    cpu_usage = get_cpu_usage()
    logger.info(cpu_usage)
    print(cpu_usage)
    return jsonify({'cpu_usage': cpu_usage})


# 登陆页面--需要和后端交互的--['GET','POST']


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # 登陆成功,重定向到首页
            return redirect(url_for('index'))
    # 渲染信息页面
    return render_template('login.html')


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
    app.run(host="0.0.0.0", debug=True)
