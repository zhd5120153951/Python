'''
@FileName   :functions.py
@Description:
@Date       :2023/11/22 16:22:51
@Author     :daito
@Website    :Https://github.com/zhd5120153951
@Copyright  :daito
@License    :None
@version    :1.0
@Email      :2462491568@qq.com
'''
# 登陆功能
from flask import request, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from app import DATABASE


def login():
    username = request.form.get('username')
    password = request.form.get('password')

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE username = ?', (username, ))
        user = cursor.fetchone()

    if user and check_password_hash(user[2], password):
        session['username'] = username
        return 1
    else:
        return "账号或密码不对,请验证后再试."
