from flask import Flask, render_template, request, make_response, redirect
from extensions import register_extensions, db
from config import Config
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, get_current_user, unset_jwt_cookies
from models import User, Student
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


@app.route('/dash')
@jwt_required()
def dash_view():
    return render_template('dash.html')


@app.route('/rights')
@jwt_required()
def rights_view():
    return render_template('rights.html')


@app.route('/role')
@jwt_required()
def role_view():
    return render_template('role.html')


@app.route('/dept')
@jwt_required()
def dept_view():
    return render_template('dept.html')


@app.route('/user')
@jwt_required()
def user_view():
    return render_template('user.html')


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
    print(username)
    # password = data['password']
    q = db.select(User).where(User.username == username)
    user = db.session.execute(q).scalar()
    print(user)
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
    access_token = create_access_token(user)
    response = make_response({
        'code': 0,
        'msg': '登陆成功',
        'access_token': access_token
    })
    set_access_cookies(response, access_token)
    return response


@app.get('/student_view')  # 相当于一点击就要发送请求渲染表格
def student_view():
    return render_template('student_view.html')


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
