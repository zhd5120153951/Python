from flask import Flask, render_template, request, make_response, redirect
from extensions import register_extensions, db
from config import Config
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, get_current_user, unset_jwt_cookies
from models import User, Student, Camera
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "daito_yolov5_flask"  # 使用craete_access_token必须要配置这个
register_extensions(app)


@app.route('/')
@jwt_required()
def index():
    current_user: User = get_current_user()
    return render_template('index.html', current_user=current_user)


'''系统管理功能'''


@app.route('/system_manage/backgroud_page')
@jwt_required()
def backgroud_page_view():
    return render_template('system_manage/backgroud_page.html')


@app.route('/system_manage/manage_center')
@jwt_required()
def manage_center_view():
    return render_template('system_manage/manage_center.html')


@app.route('/system_manage/system_setting')
@jwt_required()
def system_setting_view():
    return render_template('system_manage/system_setting.html')


'''设备管理功能'''


# @app.route('/device_manage/add')
@app.get('/device_manage/add')
@jwt_required()
def add_view():
    return render_template('device_manage/add.html')


@app.post('/addcamera')  # 处理添加摄像头
def add_camera():
    print("add camera")
    data = request.get_json()
    camera = Camera()
    camera.name = data['cameraname']
    camera.url = data['rtspurl']
    db.session.add(camera)
    db.session.commit()
    return {
        'code': 0,
        'msg': '添加成功'
    }


@app.route('/device_manage/preview')
@jwt_required()  # 登陆权限检查
def preview_view():
    return render_template('device_manage/preview.html')


@app.route('/device_manage/manage')
@jwt_required()  # 登陆权限检查
def manage_view():
    return render_template('device_manage/manage.html')


@app.route('/device_manage/control')
@jwt_required()  # 登陆权限检查
def control_view():
    return render_template('device_manage/control.html')


'''算法管理功能'''


@app.route('/algorithm_manage/config')
@jwt_required()
def config_view():
    return render_template('algorithm_manage/config.html')


@app.route('/algorithm_manage/check')
@jwt_required()
def check_view():
    return render_template('algorithm_manage/check.html')


'''报警管理功能'''


@app.get('/alarm/student_view')  # 相当于一点击就要发送请求渲染表格--从服务器获取数据
@jwt_required()
def student_view():
    return render_template('alarm/student_view.html')


@app.route('/preview')
def preview():
    return render_template('preview.html')


@app.get('/student')
def get_student_list():
    # 分页信息获取
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("limit", type=int, default=10)

    q = db.select(Student)

    name = request.args.get('name')
    address = request.args.get('address')
    if name:
        q = q.where(Student.name.like(f'%{name}%'))
    if address:
        q = q.where(Student.address.like(f'%{address}%'))

    student_pag = db.paginate(q, page=page, per_page=per_page, error_out=False)

    return {
        "code": 0,
        "message": "",
        "count": student_pag.total,
        "data": [
            {
                "id": student.id,
                "name": student.name,
                "username": student.username,
                "sex": student.sex,
                "birthdate": str(student.birthdate),
                "address": student.address,
                "mail": student.mail,
            }
            for student in student_pag.items
        ],
        "status": "success",
    }


@app.post('/student')
def create_student():
    data = request.get_json()
    del data['id']  # 删除多余的 id

    # sqlite 的日期必须接受对象，MySQL可以直接处理字符串
    if data['birthdate']:
        data['birthdate'] = datetime.strptime(data['birthdate'], '%Y-%m-%d')
    else:
        del data['birthdate']

    # 解包初始化
    stu = Student(**data)
    db.session.add(stu)
    db.session.commit()
    return {
        'code': 0,
        'message': '新增数据成功'
    }


@app.put('/student/<int:sid>')
def update_student(sid):
    data = request.get_json()
    del data['id']
    if data['birthdate']:
        data['birthdate'] = datetime.strptime(data['birthdate'], '%Y-%m-%d')
    else:
        del data['birthdate']

    stu = Student.query.get(sid)
    for key, value in data.items():
        setattr(stu, key, value)
    db.session.commit()
    return {
        'code': 0,
        'message': '修改数据成功'
    }


@app.delete('/student/<int:sid>')
def delete_student(sid):
    stu = Student.query.get(sid)
    db.session.delete(stu)
    db.session.commit()
    return {
        'code': 0,
        'message': '删除数据成功'
    }


@app.get('/register')
def register_view():
    return render_template('register.html')


@app.post('/register')
def register_post():
    data = request.get_json()
    user = User()
    user.name = data['username']
    user.username = data['username']
    user.password = data['password']
    db.session.add(user)
    db.session.commit()
    return {
        'code': 0,
        'msg': '注册成功'
    }


@app.get('/login')
def login_view():
    return render_template('login.html')


@app.post('/login')
def login_post():
    data = request.get_json()
    username = data['username']
    # password = data['password']
    q = db.select(User).where(User.username == username)
    user = db.session.execute(q).scalar()
    if not user:
        return {
            'code': -1,
            'msg': '该用户不存在'
        }
    if user.password != data['password']:
        return {
            'code': -1,
            'msg': '密码错误'
        }
    # 对当前用户的访问加密
    access_token = create_access_token(user)
    response = make_response({
        'code': 0,
        'msg': '登陆成功',
        'access_token': access_token
    })
    set_access_cookies(response, access_token)
    # print(response)  # 结果：<Response 398 bytes [200 OK]>
    return response


@app.cli.command()
def init():
    db.drop_all()
    db.create_all()
    u1 = User(username='admin', passsword='admin888')
    u2 = User(username='daito', passsword='admin888')

    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()

    import faker
    fake = faker.Faker('zh-CN')
    for i in range(1, 101):
        data = fake.simple_profile(sex=None)
        obj = Student(**data)
        db.session.add(obj)
    db.session.commit()


@app.route('/logout', methods=['GET', 'POST'])
@jwt_required()
def logout():
    response = make_response(redirect('/login'))
    unset_jwt_cookies(response)
    return response


# 应该用蓝图的方式呈现--不要把所有的代码写在app.py中
if __name__ == "__main__":
    app.run(debug=True)
