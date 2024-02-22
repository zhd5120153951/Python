import base64
import requests
from multiprocessing import Array, Lock, Manager
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, user_accessed
from flask_wtf import FlaskForm
from sqlalchemy import exists
import torch
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import cv2
import psutil
from ipaddress import ip_address, AddressValueError
import netifaces
import socket
import json
import multiprocessing as mp  # 推理时用多进程
import threading  # 预览时用多线程
import datetime
import os
import re
import time
import tkinter as tk
from detect_plate import get_parser, load_model, init_model, detect_Recognition_plate, draw_result

# logging模块不跨进程--单进程或者多线程使用
# 配置基本日志设置
# logging.basicConfig(
#     level=logging.DEBUG,  # 设置日志级别，可以选择DEBUG, INFO, WARNING, ERROR, CRITICAL
#     # 设置日志消息的格式
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',  # 设置日期时间格式
#     filename='./App.log',  # 指定日志输出到文件
#     filemode='w'  # 指定文件写入模式(a表示追加，w表示覆盖)
# )
# 创建一个日志记录器
# logger = logging.getLogger('my_logger')


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

# 创建数据库users.db;再是用户登陆信息表users;流地址信息表rtsps


def create_table():
    with sqlite3.connect("users.db") as conn:  # 这个的本质就是返回一个对象
        cursor = conn.cursor()  # 获取游标
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            );''')
        cursor.execute(
            f'''CREATE TABLE IF NOT EXISTS rtsps (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            rtsp_url TEXT NOT NULL
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

            conn.commit()

        if isExistUser and check_password_hash(isExistUser[2], password):
            return redirect(url_for('homepage'))  # redirect()是某个页面的路由函数

        flash('Invalid username or password', 'info')
        return redirect(url_for('home'))
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
        # print(password)
        hashed_password = generate_password_hash(password)
        # print(hashed_password)
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


# 路由--获取rtsp视频--暂时不用这个


@app.route('/video_feed')
def video_feed():
    isVideo = True
    return Response(generate_frames(isVideo), mimetype='multipart/x-mixed-replace; boundary=frame')

# 路由：获取 CPU 使用率的 API--由jquery发起


@app.route('/get_resources')
def get_system_usage():

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_cap = psutil.cpu_freq().current/1000
    # print(cpu_cap)
    memory_info = psutil.virtual_memory().percent
    # Linux系统
    # disk_info = psutil.disk_usage('/').percent

    # windows系统
    disk_info_e = psutil.disk_usage('E:/').percent  # Linux下
    disk_info_c = psutil.disk_usage('C:/').percent  # Linux下
    disk_info_d = psutil.disk_usage('D:/').percent  # Linux下
    disk_info = round((disk_info_c+disk_info_e+disk_info_d)/3, 2)

    # 获取总内存和总磁盘空间
    memory_cap = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # 转换为GB
    # disk_cap = psutil.disk_usage('/').total / (1024 ** 3)  # 转换为GB
    disk_cap_c = psutil.disk_usage('C:/').total / (1024 ** 3)  # 转换为GB
    disk_cap_d = psutil.disk_usage('D:/').total / (1024 ** 3)  # 转换为GB
    disk_cap_e = psutil.disk_usage('E:/').total / (1024 ** 3)  # 转换为GB
    disk_cap = round((disk_cap_c+disk_cap_d+disk_cap_e)/3, 2)

    data = {
        # 'sys': sys_maintain,
        'cpu': cpu_usage,
        'memory': memory_info,
        'disk': disk_info,
        'cpu_cap': cpu_cap,
        'memory_cap': memory_cap,
        'disk_cap': disk_cap,
    }

    # print(data)
    return jsonify(data)

# 获取IP


def get_ip_addr():
    ip_addr = {"local_ip": ""}
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # print(s)
    # 尝试连接非存在地址，来激活网络接口的 IP
    try:
        # 这里的地址不需要真实存在
        s.connect(("10.255.255.255", 1))
        ip_addr['local_ip'] = s.getsockname()[0]

        # print(ip_addr['local_ip'])
        # print(s.getsockname()[1])

    except:
        create_notification("获取设备IP失败")
        ip_addr['local_ip'] = 'N/A'
    s.close()
    return ip_addr
# 路由--ip_config


@app.route('/ip_config', methods=['GET', 'POST'])
def ip_config():
    ip_addr = get_ip_addr()
    return render_template("ip_config.html", ip_addr=ip_addr)


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
        interface = "eth0"  # Linux系统
        # print(new_ip)
        if set_ip_addr(interface, new_ip):
            return redirect(url_for("ip_config"))
        else:
            create_notification("ip设置失败,请检查后重试!")
# 路由--rtsp_config


@app.route('/rtsp_config')
def rtsp_config():
    # 获取当前的摄像头rtsp
    return render_template("rtsp_config.html")


# 预览


def Preview(username, password, rtsp_url, index):
    url = f"rtsp://{username}:{password}@{rtsp_url}:554/Streaming/Channels/101"
    # 使用OpenCV打开视频流
    cap = cv2.VideoCapture(url)
    winname = "preview_" + index
    # 创建一个窗口来显示视频流
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    while True:
        # 读取视频帧
        ret, frame = cap.read()

        if not ret:
            break
        # 实时显示视频帧
        cv2.imshow(winname, frame)
        # 按下esc键退出预览
        # if cv2.waitKey(1) == 27:
        #     break

        # 点击窗口X按钮退出预览
        cv2.waitKey(1)
        if cv2.getWindowProperty(winname, cv2.WND_PROP_VISIBLE) < 1:
            break
    # 释放视频流和关闭窗口
    cap.release()
    cv2.destroyAllWindows()

# 消息弹窗


def create_notification(message):
    root = tk.Tk()
    root.overrideredirect(True)  # 隐藏标题栏和边框
    root.attributes("-topmost", True)  # 始终置于顶层
    root.geometry("300x100+{}+{}".format(
        root.winfo_screenwidth() - 300, root.winfo_screenheight()-100))  # 设置窗口位置和大小
    label = tk.Label(root, text=message)
    label.pack(pady=20)

    def close_notofication():
        root.destroy()
    # 设置定时器,3秒后自动关闭
    root.after(3000, close_notofication)

    root.mainloop()


@app.route('/set_rtsp', methods=['GET', 'POST'])
def set_rtsp():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    if request.method == "POST":
        # btn_value = request.form.get("button","")
        btn_value = request.form.get("button")
        # print(btn_value)
        form_data_1 = request.form.get("new_rtsp_1")
        # print(form_data_1)
        form_data_2 = request.form.get("new_rtsp_2")
        # print(form_data_2)

        global rtsp_dict

        # 把rtsp保存到json中存起来,AI设置中的参数,开关也是如此,后面把模型加载时从json中读取
        if btn_value == "btn_1":
            cursor.execute("UPDATE rtsps SET id=1,username=?,password=?,rtsp_url=? WHERE rowid=1",
                           ("admin", "jiankong123", form_data_1))
            conn.commit()

            flash("rtsp_1设置成功")
            with lock:
                shared_arr[0] = True

        if btn_value == "btn_2":
            cursor.execute("UPDATE rtsps SET id=2,username=?,password=?,rtsp_url=? WHERE rowid=2",
                           ("admin", "jiankong123", form_data_2))
            conn.commit()

            flash("rtsp_2设置成功")
            with lock:
                shared_arr[0] = True

        if btn_value == "prev_1":  # 用多线程预览--后面在改进
            cursor.execute('SELECT * FROM rtsps WHERE id = 1')  # 编号为1的只有一个
            isExistId = cursor.fetchone()  # 所以用fetchone()

            if isExistId:  # 存在rtsp
                th_prev = threading.Thread(target=Preview, args=(
                    isExistId[1], isExistId[2], isExistId[3], isExistId[0]))
                th_prev.start()

            else:  # 可以给个弹窗提示
                create_notification("没有对应的id=1摄像头流")

        if btn_value == "prev_2":  # 用多线程预览--后面在改进--而且这里必须要用多线程或者多进程
            cursor.execute('SELECT * FROM rtsps WHERE id = 2')  # 编号为1的只有一个
            isExistId = cursor.fetchone()  # 所以用fetchone()

            if isExistId:  # 存在rtsp
                th_prev = threading.Thread(target=Preview, args=(
                    isExistId[1], isExistId[2], isExistId[3], isExistId[0]))
                th_prev.start()
            else:
                create_notification("没有对应id=2摄像头的流")
    else:
        # 首次请求或者GET请求时，渲染表单并传入上次输入的值
        form_data_1 = request.args.get('new_rtsp_1', '')
        form_data_2 = request.args.get('new_rtsp_2', '')
    # 数据库关闭
    cursor.close()
    conn.close()

    return render_template("rtsp_config.html", new_rtsp_1=form_data_1, new_rtsp_2=form_data_2)

# 路由--system_resource


@app.route('/system_resource')
def system_resource():
    return render_template("system_resource.html")


# 路由--rtsp_config


@app.route('/ai_setting')
def ai_setting():
    return render_template("ai_setting.html")


@app.route('/set_ai', methods=["GET", "POST"])
def set_ai():
    global shared_arr, lock
    if request.method == "POST":
        # btn_value = request.form.get("button","")
        btn_value = request.form.get("button")
        # print(btn_value)
        gap_det = request.form.get("gap_det")
        # print(form_data_1)

        global ai_dict

        # 把rtsp保存到json中存起来,AI设置中的参数,开关也是如此,后面把模型加载时从json中读取
        if btn_value == "btn_ok":
            # 打开json文件
            with open("ai_config.json", "w") as file:
                #  将RTSP地址保存到JSON文件
                ai_dict['gap_det'] = int(gap_det)
                # json.dump(data_1,  file)
                json.dump(ai_dict, file)
                file.close()
                flash("ai配置设置成功")
            # 通知子进程ai设置已更新,可以读取新的设置参数推理
            with lock:
                # 加锁，主进程改变共享数组的值:index-0-rtsp;index-1-ai
                shared_arr[1] = True
                # print("主进程改变共享数组的值为:", list(shared_arr))

    else:
        # 首次请求或者GET请求时，渲染表单并传入上次输入的值
        gap_det = request.args.get('gap_det', '')

    return render_template("ai_setting.html", gap_det=gap_det)


# 判断一个IP地址是否合规
def is_valid_ip(ip_address):
    # 使用正则表达式匹配IP地址的格式
    pattern = '^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(pattern, ip_address):
        return True
    else:
        return False
# 获取图像函数--有两路摄像头就开两个进程
# 区域入侵用的是队列--向两个进程传图
# 这次用Manager


def get_frame(q_img, shared_arr):
    print("get_frame process pid:%s" % os.getpid())
    url = None
    cap_1 = None
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rtsps WHERE id = 1')
    isExistId = cursor.fetchone()

    if isExistId:  # 初始就配好流地址
        if is_valid_ip(isExistId[3]):
            url = f"rtsp://{isExistId[1]}:{isExistId[2]}@{isExistId[3]}:554/Streaming/Channels/101"
            cap_1 = cv2.VideoCapture(url)
            # cap_1 = cv2.VideoCapture("rtsp://127.0.0.1:9554/live/test")#临时测试用
        else:
            create_notification("初始流地址出错,请检查后再试!")
            cap_1 = cv2.VideoCapture(0)  # 流地址不合规,用本地
    else:
        cap_1 = cv2.VideoCapture(0)  # 本地摄像头
    with open("ai_config.json", mode="r") as f_ai:
        det_gap = json.load(f_ai)["gap_det"]
        f_ai.close()
    cursor.close()
    conn.close()
    num = 0
    while True:
        if shared_arr[1]:  # 读取ai配置--标志位:在ai配置页面确定后置为真
            with open("ai_config.json", mode="r") as f_ai:
                det_gap = json.load(f_ai)["gap_det"]
                f_ai.close()
            shared_arr[1] = False

        if shared_arr[0]:  # 读取rtsp配置
            cap_1.release()
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM rtsps WHERE id = 1')
            isExistId = cursor.fetchone()
            if isExistId:
                if is_valid_ip(isExistId[3]):
                    shared_arr[0] = False
                    url = f"rtsp://{isExistId[1]}:{isExistId[2]}@{isExistId[3]}:554/Streaming/Channels/101"
                    cap_1 = cv2.VideoCapture(url)
                else:
                    create_notification("配置的流地址出错,请重新配置!")
                    cap_1 = cv2.VideoCapture(0)
                cursor.close()
                conn.close()
            else:
                cursor.close()
                conn.close()
                continue  # 数据库中没找到流地址
        if cap_1.isOpened():
            if num % 24 != 0:
                frame = cap_1.read()
                num += 1
                continue

            # ret_1, frame_1 = cap_1.read()
            q_img.put(cap_1.read()[1])
            print("读一帧")
            if q_img.qsize() > 10:
                q_img.get()
            if num % 24 == 0:
                num = 1

        else:
            cap_1.release()
            cap_1 = cv2.VideoCapture(url)


# image转base64编码


def img2base64(img):
    encode_img = base64.b64encode(img)
    return encode_img.decode("utf-8")  # 把byte转换为字符串


# 车牌检测,识别----推理速度要快于取流速度(让队列趋向于0,如果趋向于10的话丢弃的帧会累计越多)


# def det_rec_model(det_model, q_img, device, rec_model, img_size, is_color):
def det_rec_model(q_img):
    print("det_rec_model process pid:%s" % os.getpid())
    # 参数
    opt = get_parser()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # 可以暂时不要--因为会上传到服务端
    if not os.path.exists(opt.output):
        os.mkdir(opt.output)
    # 检测模型加载
    det_model = load_model(opt.detect_model, device)
    # 识别模型加载
    rec_model = init_model(device, opt.rec_model, opt.is_color)
    # 参数量计算
    total_det = sum(p.numel() for p in det_model.parameters())
    total_rec = sum(p.numel() for p in rec_model.parameters())
    print("detect model params: %.2fM,rec model params: %.2fM" %
          (total_det / 1e6, total_rec / 1e6))

    cn = 1
    # 隔几秒检测一次,但是这里只推理,隔几秒的图由读图子进程控制
    while True:
        if q_img.qsize() == 0:
            # print("inference proc", q_img.qsize())
            # time.sleep(0.04)  # 等待抓图进程取流
            # cv2.waitKey(500)
            continue
        else:
            print("推理一帧")
            frame = q_img.get()
            t1 = cv2.getTickCount()  # 推理前时钟频率
            dict_list = detect_Recognition_plate(
                det_model, frame, device, rec_model, opt.img_size, is_color=opt.is_color)
            t2 = cv2.getTickCount()  # 推理后时钟频率

            if len(dict_list) == 0:  # 没检测到车牌--跳过
                continue

            ori_img = draw_result(frame, dict_list)
            infer_time = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / infer_time
            str_fps = f'fps:{fps:.4f}'

            cv2.putText(ori_img, str_fps, (20, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # cv2.imwrite("ret.jpg", ori_img)
            if len(dict_list) != 0:
                cv2.imwrite(
                    "E:\\Source\\Web\\"+str(cn)+".jpg", ori_img)
                cn += 1

            # else:
            #     # 发送post请求给服务端
            #     #  获取当前时间
            #     now_time = datetime.datetime.now()

            #     #  格式化时间
            #     formatted_time = now_time.strftime("%Y-%m-%d  %H:%M:%S")
            #     encode_img = img2base64(ori_img)
            #     data = {
            #         "date": formatted_time,
            #         "encode_img": encode_img
            #     }
            #     header = {
            #         "Content-Type": "application/json;charset=utf-8"
            #     }
            #     try:
            #         ret = requests.post(
            #             "http://47.108.165.167/prod-api/system/kaoqin", json.dumps(data), headers=header)
            #         print(ret)
            #     except Exception as e:
            #         print(e)


if __name__ == '__main__':
    # 初始化全局变量
    create_table()

    # 多进程部分
    q_img = mp.Queue(maxsize=10)  # 装图像的队列--目前只要一个摄像头
    # 共享数组Array--is_rtsp_config,is_ai_config
    shared_arr = Array('b', [False, False])
    lock = Lock()
    # init
    mp.set_start_method('spawn', force=True)

    # 开启两个子进程--取流和推理
    proc_get = mp.Process(target=get_frame, args=(
        q_img, shared_arr))
    # 参数可以传递进子进程,但是模型需要在里面加载
    proc_infer = mp.Process(target=det_rec_model, args=(q_img,))

    proc_get.daemon = True  # 设为主进程的守护进程,主进程结束,这两个也结束
    proc_infer.daemon = True

    proc_get.start()
    proc_infer.start()

    # 设备管理界面的相关参数*******************
    ai_dict = {"gap_det": None}  # Ai配置字典--还有scoreThreshold,nmsThreshold

    # join()是阻塞:表示让主进程等待子进程结束之后，再执行主进程。

    # debug=True表示代码右边动会自动重启子进程
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
    # app.run()默认启用Werkzeug，生成一个子进程，作用是当代码有变动的时候自动重启--所以会有两个推理进程和取图进程
    # app.run(host="0.0.0.0", debug=True)
