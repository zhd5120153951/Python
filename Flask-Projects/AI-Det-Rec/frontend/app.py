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
# from detect_plate import get_parser, load_model, init_model, detect_Recognition_plate, draw_result

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


@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    # 初始化全局变量
    # create_table()

    # 多进程部分
    # q_img = mp.Queue(maxsize=10)  # 装图像的队列--目前只要一个摄像头
    # 共享数组Array--is_rtsp_config,is_ai_config
    # shared_arr = Array('b', [False, False])
    # lock = Lock()
    # init
    # mp.set_start_method('spawn', force=True)

    # 开启两个子进程--取流和推理
    # proc_get = mp.Process(target=get_frame, args=(
    #     q_img, shared_arr))
    # 参数可以传递进子进程,但是模型需要在里面加载
    # proc_infer = mp.Process(target=det_rec_model, args=(q_img,))

    # proc_get.daemon = True  # 设为主进程的守护进程,主进程结束,这两个也结束
    # proc_infer.daemon = True

    # proc_get.start()
    # proc_infer.start()

    # 设备管理界面的相关参数*******************
    # ai_dict = {"gap_det": None}  # Ai配置字典--还有scoreThreshold,nmsThreshold

    # join()是阻塞:表示让主进程等待子进程结束之后，再执行主进程。

    # debug=True表示代码右边动会自动重启子进程
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    # app.run()默认启用Werkzeug，生成一个子进程，作用是当代码有变动的时候自动重启--所以会有两个推理进程和取图进程
    # app.run(host="0.0.0.0", debug=True)
