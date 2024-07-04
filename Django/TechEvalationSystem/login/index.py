

# 登录页面
def login(request):
    '''
    登录页面
    #GET请求{
        返回登录页面
        }
    #POST请求{
        登录操作
        1.处理提交数据
            >两次输入的密码要一致
            >当前用户是否可用
            插入数据【先铭文处理密码】
        }
    :param request:
    :return:
    '''
    if request.method == 'GET':
        # 检查session，如果登录了跳转学生评价首页
        if request.session.get('xuehao'):
            return HttpResponseRedirect('/pingjia/')
        # 检查session，如果登录了跳转教师首页
        if request.session.get('teacher_id'):
            return HttpResponseRedirect('/teacher/index')

        # 检查Cookies，如果登录了显示已登录
        s_xuehao = request.COOKIES.get('xuehao')
        if s_xuehao:
            # 学号回写session
            request.session['xuehao'] = s_xuehao
            return HttpResponseRedirect('/pingjia/')

        # 检查Cookies，如果登录了显示已登录
        teacher_id = request.COOKIES.get('teacher_id')
        if teacher_id:
            # 学号回写session
            request.session['teacher_id'] = teacher_id
            return HttpResponseRedirect('/teacher_index/')

        # GET返回页面
        return render(request, 'pingjiaxitong/login.html')
    elif request.method == 'POST':
        xuehao = request.POST['xuehao']
        password = request.POST['password']
        msg = '请输入一个正确的用户名和密码,注意他们都是区分大小写的!'

        # 哈希算法
        # m = hashlib.md5()
        # m.update(password.encode())
        # password_m = m.hexdigest()
        password_m = password

        try:
            b1 = Students.objects.filter(xuehao=xuehao, password=password_m)

        except Exception as e:
            print('--login xuehao error %s' % (e))

        if b1:
            request.session['xuehao'] = str(xuehao)
            # request.session['xuehao'] = b1.name
            resp = HttpResponseRedirect('/pingjia/')
            if 'remember' in request.POST:
                resp.set_cookie('xuehao', xuehao, 3600 * 24 * 3)

            return resp
        try:
            t1 = Teachers.objects.filter(teacher_id=xuehao, password=password_m)

        except Exception as e:
            print('--login xuehao error %s' % (e))
        if t1:
            request.session['teacher_id'] = str(xuehao)
            resp = HttpResponseRedirect('/teacher_index')
            if 'remember' in request.POST:
                resp.set_cookie('teacher_id', xuehao, 3600 * 24 * 3)
            return resp

        return render(request, 'pingjiaxitong/login.html', locals())


# 退出登录

def logout(request):
    # 删除session
    if 'xuehao' in request.session:
        del request.session['xuehao']
    if 'teacher_id' in request.session:
        del request.session['teacher_id']

    # 删除cookies
    resp = HttpResponseRedirect('/')
    if 'xuehao' in request.COOKIES:
        resp.delete_cookie('xuehao')
    if 'teacher_id' in request.COOKIES:
        resp.delete_cookie('teacher_id')
    return resp


# 注册页面
def zhuce(request):
    if request.method == 'GET':
        return render(request, 'pingjiaxitong/zhuce.html')
    elif request.method == 'POST':
        xuehao = request.POST['xuehao']
        password = request.POST['password']
        password_1 = request.POST['password_1']
        if password != password_1:
            # return HttpResponse('密码不一致！！！')
            msg = '密码不一致！！！'
            return render(request, "pingjiaxitong/zhuce.html", locals())
        s = Students.objects.filter(xuehao=xuehao)
        if s:
            # return HttpResponse('学号已注册！')
            msg = '学号已注册！'
            return render(request, 'pingjiaxitong/zhuce.html', locals())
        # 哈希算法
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        try:
            xuehao = Students.objects.create(xuehao=xuehao, password=password_m)
        except Exception as e:
            # 有可能报错-重复插入【唯一索引并发写入问题】
            print('---create user is error%S' % (e))
            msg = '学号已注册！'
            return render(request, 'pingjiaxitong/zhuce.html', locals())
        # 免登录一天

        request.session['xuehao'] = str(xuehao.xuehao)
        # request.session['id'] = xuehao.id
        # TODO修改session存储时间为一天
        # 记住我 可以免登录三天
        resp = HttpResponseRedirect('/pingjia/')
        if 'remember' in request.POST:
            resp.set_cookie('xuehao', xuehao, 3600 * 24 * 3)
            # resp.set_cookie('id',Students.id, 3600 * 24 * 3)

        return resp

        return HttpResponseRedirect('/pingjia/')


# 修改密码页面

def update_password(request):
    if request.method == 'GET':

        return render(request, 'pingjiaxitong/update_password.html')
    elif request.method == 'POST':
        xuehao = request.session['xuehao']
        pswd = request.POST['password']
        pswd_1 = request.POST['password_1']
        pswd_2 = request.POST['password_2']

        # 哈希算法
        # m = hashlib.md5()
        # m.update(pswd.encode())
        # password_m = m.hexdigest()

        # 原密码是否相同
        if pswd_1 != pswd_2:
            # return HttpResponse('密码不一致！！！')
            msg = '密码不一致！！！'
            return render(request, "pingjiaxitong/update_password.html", locals())
        try:
            s = Students.objects.filter(xuehao=xuehao, password=pswd_1)
        except Exception as e:
            return HttpResponse('报错', e)

        # 哈希算法
        # m = hashlib.md5()
        # m.update(pswd_1.encode())
        # password_m = m.hexdigest()
        # 是否账号密码一样
        if s:
            # 如果是修改密码
            s.update(password=pswd_1)
            # 免登录一天
            request.session['xuehao'] = xuehao

            msg = '修改密码成功！'

            return HttpResponseRedirect('/pingjia/', locals())
        else:
            msg = '密码错误！'
            return render(request, 'pingjiaxitong/update_password.html', locals())


# 教师注册页面
def teacher_zhuce(request):
    if request.method == 'GET':
        return render(request, 'teacher/zhuce.html')
    elif request.method == 'POST':
        teacher_id = request.POST['teacher_id']
        password = request.POST['password']
        password_1 = request.POST['password_1']
        if password != password_1:
            # return HttpResponse('密码不一致！！！')
            msg = '密码不一致！！！'
            return render(request, "teacher/zhuce.html", locals())
        s = Teachers.objects.filter(teacher_id=teacher_id)
        if s:
            # return HttpResponse('教工号已注册！')
            msg = '教工号已注册！'
            return render(request, 'teacher/zhuce.html', locals())
        # 哈希算法
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        try:
            teacher = Teachers.objects.create(teacher_id=teacher_id, password=password_m)
        except Exception as e:
            # 有可能报错-重复插入【唯一索引并发写入问题】
            print('---create user is error%S' % (e))
            msg = '教工号已注册！'
            return render(request, 'teacher/zhuce.html', locals())
        # 免登录一天

        request.session['teacher_id'] = str(teacher.teacher_id)

        # 记住我 可以免登录三天
        resp = HttpResponse('记住我🆗')
        if 'remember' in request.POST:
            resp.set_cookie('teacher_id', teacher_id, 3600 * 24 * 3)
            # resp.set_cookie('id',Students.id, 3600 * 24 * 3)

        return resp

        # TODO修改session存储时间为一天

        return HttpResponse('ok123')