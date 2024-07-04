import hashlib

from django.shortcuts import render, HttpResponse, HttpResponseRedirect

from login.models import *


# Create your views here.
# def check_login(fn):
#     def wrap(request, *args, **kwargs):
#         status = request.session.get('xuehao')
#         if not status:  # 报错
#             s_xuehao = request.COOKIES.get('xuehao')
#             if not s_xuehao:
#                 # 查询教师
#                 # status = request.session.get('teacher_id')
#                 # if not status:
#                 # teacher_id = request.COOKIES.get('teacher_id')
#                 # if not teacher_id:
#                 return HttpResponseRedirect('/login/')
#                 # return HttpResponseRedirect('/login/')
#                 # else:
#                 # 教工号回写session
#                 # request.session['teacher_id'] = teacher_id
#
#             else:
#                 # 学号回写session
#
#                 request.session['xuehao'] = s_xuehao
#
#         return fn(request, *args, **kwargs)
#
#     return wrap


# Create your views here.
# 系统首页
# @check_login
def index(request):
    # get请求返回页面
    if request.method == "GET":
        xuehao = request.session['xuehao']
        # tiku = TiKu_1.objects.filter(is_active=True)
        book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no').order_by('id')  #
        book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok')
        return render(request, 'students/index.html', locals())


# 学生评功能
def update_pingjia(request, kecheng_id):
    xuehao = request.session['xuehao']
    try:
        # kecheng = KeCheng.objects.get(id=kecheng_id)
        kecheng = KeCheng.objects.filter(id=str(kecheng_id), is_active=True).values('id', 'kecheng', 'teacher_id__name',
                                                                                    'teacher_id__phone')
        tiku = TiKu_1.objects.filter(is_active=True).order_by('id')
        book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no').order_by('id')
        book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok')
    except Exception as e:
        print('--update  book error is %s' % (e))
        return HttpResponse('--The kecheng is not existed!')

    if request.method == 'GET':

        return render(request, 'students/pingjia_id.html', locals())

    # post请求处理评价保存到评价库
    elif request.method == 'POST':
        # 按题库写到评价库
        tiku = TiKu_1.objects.filter(is_active=True)
        stu_liuyan = request.POST['liuyan']
        s_a = 1
        sum = 0
        for i in tiku:
            # print(int(i.id))

            stu_daan = request.POST[str(i.id)]
            # print(stu_daan, type(stu_daan))
            sum += round(float(stu_daan))

            try:
                a = PingJia.objects.filter(id=kecheng_id)

            except Exception as e:
                print(e)
            try:
                b = PingJia.objects.get(id=kecheng_id)

            except Exception as e:
                print(e)

            if a:

                if s_a == 2:
                    b.s_daan2 = stu_daan
                    s_a += 1
                    b.save()
                    continue

                if s_a == 3:
                    b.s_daan3 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 4:
                    b.s_daan4 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 5:
                    b.s_daan5 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 6:
                    b.s_daan6 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 7:
                    b.s_daan7 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 8:
                    b.s_daan8 = stu_daan
                    s_a += 1
                    b.save()
                    continue

                if s_a == 9:
                    b.s_daan9 = stu_daan
                    s_a += 1
                    b.save()
                    continue
                if s_a == 10:
                    b.s_daan10 = stu_daan
                    s_a += 1
                    b.save()
                    continue

            else:

                try:
                    a = PingJia.objects.create(id=kecheng_id,
                                               s_daan1=stu_daan,
                                               kecheng=KeCheng.objects.get(id=kecheng_id),
                                               s_liuyan=stu_liuyan,
                                               is_active=True)
                except Exception as e:
                    print('添加评价库失败！%s' % e)

                # print('保存第一个成功')
                # 课程表库里更新是否评价——————是
                try:
                    c = KeCheng.objects.get(id=str(kecheng_id))
                except Exception as e:
                    print(e)
                c.ok = 'ok'
                c.save()
                s_a += 1
                # print(s_a)
        avg = sum / (s_a - 1)
        # print('%s-%s-%s' % (sum, s_a - 1, avg))
        b.s_avg = float('%.2f' % avg)
        b.save()

        return HttpResponseRedirect('/students/')


# 学生已评价
# @check_login
def ok_pingjia(request):
    xuehao = request.session['xuehao']
    tiku = TiKu_1.objects.filter(is_active=True)
    book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no')  #
    book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok').order_by('id')  #
    return render(request, 'students/ok_pingjia.html', locals())


# 学生查看已评价
# @check_login
def cat_pingjia(request, kecheng_id):
    xuehao = request.session['xuehao']
    book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no')  #
    book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok').order_by('id')  #
    kecheng = KeCheng.objects.filter(id=str(kecheng_id), is_active=True).values('id', 'kecheng', 'teacher_id__name',
                                                                                'teacher_id__phone')
    tiku = TiKu_1.objects.filter(is_active=True)

    data_list = list()
    pj = PingJia.objects.get(id=kecheng_id, kecheng__xuehao=xuehao)
    s_a = 1

    """
    1.显示答案
        显示评价id
        显示评价题
        学生答案
    
    """

    return render(request, 'students/cat_pingjia.html', locals())


# 学生密码修改
def update_password(request):
    if request.method == 'GET':

        return render(request, 'students/update_password.html')
    elif request.method == 'POST':
        xuehao = request.session['xuehao']
        pswd = request.POST['password']
        pswd_1 = request.POST['password_1']
        pswd_2 = request.POST['password_2']

        # 哈希算法
        m = hashlib.md5()
        m.update(pswd.encode())
        password_m = m.hexdigest()

        # 新密码是否相同
        if pswd_1 != pswd_2:
            # return HttpResponse('密码不一致！！！')
            msg = '密码不一致！！！'
            return render(request, "students/update_password.html", locals())
        try:
            s = Students.objects.filter(xuehao=xuehao, password=password_m)
        except Exception as e:
            return HttpResponse('students_update_pswd:', e)

        if s:
            # 如果是修改密码
            # 哈希算法
            m = hashlib.md5()
            m.update(pswd_1.encode())
            password_m = m.hexdigest()
            s.update(password=password_m)
            # 免登录一天
            request.session['xuehao'] = xuehao

            msg = '修改密码成功！'

            return HttpResponseRedirect('/students/', locals())
        else:
            msg = '原密码错误！'
            return render(request, 'students/update_password.html', locals())
