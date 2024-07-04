from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from login.models import *
import hashlib


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
        # # 检查session，如果登录了跳转学生评价首页
        # if request.session.get('xuehao'):
        #     return HttpResponseRedirect('/students/')
        # # 检查session，如果登录了跳转教师首页
        # if request.session.get('teacher_id'):
        #     return HttpResponseRedirect('/teacher/')
        #
        # # 检查Cookies，如果登录了显示已登录
        # s_xuehao = request.COOKIES.get('xuehao')
        # if s_xuehao:
        #     # 学号回写session
        #     request.session['xuehao'] = s_xuehao
        #     return HttpResponseRedirect('/students/')
        #
        # # 检查Cookies，如果登录了显示已登录
        # teacher_id = request.COOKIES.get('teacher_id')
        # if teacher_id:
        #     # 学号回写session
        #     request.session['teacher_id'] = teacher_id
        #     return HttpResponseRedirect('/teachers/')

        # GET返回页面
        return HttpResponseRedirect('/')
    # POST
    elif request.method == 'POST':
        xuehao = request.POST['xuehao']
        password = request.POST['password']

        msg = '请输入一个正确的用户名和密码,注意他们都是区分大小写的!'

        # 哈希算法
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()

        try:
            b1 = Students.objects.filter(xuehao=xuehao, password=password_m)

        except Exception as e:
            print('--login xuehao error %s' % (e))

        if b1:
            request.session['xuehao'] = str(xuehao)
            # request.session['xuehao'] = b1.name
            resp = HttpResponseRedirect('/students/')
            # if 'remember' in request.POST:
            #     resp.set_cookie('xuehao', xuehao, 3600 * 24 * 3)

            return resp
        try:
            t1 = Teachers.objects.filter(teacher_id=xuehao, password=password_m)

        except Exception as e:
            print('--login teacher error %s' % (e))
        if t1:
            request.session['teacher_id'] = str(xuehao)
            resp = HttpResponseRedirect('/teachers/')
            # if 'remember' in request.POST:
            #     resp.set_cookie('teacher_id', xuehao, 3600 * 24 * 3)
            return resp
        # 管理员登录
        try:
            t1 = GuanLiYuan.objects.filter(name=xuehao, password=password_m)

        except Exception as e:
            print('--login guanliyuan error %s' % (e))
        if t1:
            request.session['name'] = str(xuehao)
            resp = HttpResponseRedirect('/myadmin/')
            # if 'remember' in request.POST:
            #     resp.set_cookie('teacher_id', xuehao, 3600 * 24 * 3)
            return resp

        return render(request, 'index.html', {"msg": msg})


# 退出登录
# @check_login
def logout(request):
    # 删除session
    if 'xuehao' in request.session:
        del request.session['xuehao']
        # print("清理学号成功！")
    if 'teacher_id' in request.session:
        del request.session['teacher_id']
        # print("清理教工号成功！")
    if 'name' in request.session:
        del request.session['name']
        # print("清理管理员成功！")

    # 删除cookies
    resp = HttpResponseRedirect('/')
    # if 'xuehao' in request.COOKIES:
    #     resp.delete_cookie('xuehao')
    # if 'teacher_id' in request.COOKIES:
    #     resp.delete_cookie('teacher_id')
    return resp


# def check_login(fn):
#     def wrap(request, *args, **kwargs):
#         status = request.session.get('xuehao')
#         if not status:  # 报错
#             s_xuehao = request.COOKIES.get('xuehao')
#             if not s_xuehao:
#                 # 查询教师
#                 status = request.session.get('teacher_id')
#                 if not status:
#                     teacher_id = request.COOKIES.get('teacher_id')
#                     if not teacher_id:
#
#                         return HttpResponseRedirect('/login/')
#                     else:
#                         # 教工号回写session
#                         request.session['teacher_id'] = teacher_id
#
#             else:
#                 # 学号回写session
#
#                 request.session['xuehao'] = s_xuehao
#
#         return fn(request, *args, **kwargs)
#
#     return wrap
#
#

# # 系统首页
# @check_login
# def pingjia(request):
#     # get请求返回页面
#     if request.method == "GET":
#         xuehao = request.session['xuehao']
#         # tiku = TiKu_1.objects.filter(is_active=True)
#         book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no').order_by('id')  #
#         book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok')
#         return render(request, 'login/index.html', locals())
#
#
# # 学生评价页
# @check_login
# def update_pingjia(request, kecheng_id):
#     xuehao = request.session['xuehao']
#     try:
#
#         kecheng = KeCheng.objects.get(id=kecheng_id)
#         tiku = TiKu_1.objects.filter(is_active=True).order_by('id')
#         book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no').order_by('id')  #
#         book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok')
#     except Exception as e:
#         print('--update  book error is %s' % (e))
#         return HttpResponse('--The kecheng is not existed!')
#
#     if request.method == 'GET':
#
#         return render(request, 'login/pingjia_id.html', locals())
#     # post请求处理评价保存到评价库
#     elif request.method == 'POST':
#         # 按题库写到评价库
#         tiku = TiKu_1.objects.filter(is_active=True)
#         stu_liuyan = request.POST['liuyan']
#         for i in tiku:
#             print(int(i.id))
#
#             stu_daan = request.POST[str(i.id)]
#
#             try:
#                 a = PingJia.objects.filter(id=kecheng_id)
#
#             except Exception as e:
#                 print(e)
#             try:
#                 b = PingJia.objects.get(id=kecheng_id)
#
#             except Exception as e:
#                 print(e)
#
#             if a:
#
#                 if int(i.id) == 2:
#                     b.s_daan2 = stu_daan
#                     b.save()
#                     print('>>>>>>>>', stu_daan, i.id)
#                 if int(i.id) == 3:
#                     b.s_daan3 = stu_daan
#                     b.save()
#                 if int(i.id) == 4:
#                     b.s_daan4 = stu_daan
#                     b.save()
#                 if int(i.id) == 5:
#                     b.s_daan5 = stu_daan
#                     b.save()
#                 if int(i.id) == 6:
#                     b.s_daan6 = stu_daan
#                     b.save()
#                 if int(i.id) == 7:
#                     b.s_daan7 = stu_daan
#                     b.save()
#                 if int(i.id) == 8:
#                     b.s_daan8 = stu_daan
#                     b.save()
#
#                 if int(i.id) == 9:
#                     b.s_daan9 = stu_daan
#                     b.save()
#                 if int(i.id) == 10:
#                     b.s_daan10 = stu_daan
#                     b.save()
#
#             else:
#                 print(kecheng_id, stu_daan, kecheng, stu_liuyan)
#                 try:
#                     a = PingJia.objects.create(id=kecheng_id,
#                                                s_daan1=stu_daan,
#                                                kecheng=kecheng,
#                                                s_liuyan=stu_liuyan,
#                                                is_active=True)
#                 except Exception as e:
#                     print('添加评价库失败！%s' % e)
#
#                 print('保存第一个成功')
#                 # 课程表库里更新是否评价——————是
#                 try:
#                     c = KeCheng.objects.get(id=str(kecheng_id))
#                 except Exception as e:
#                     print(e)
#                 c.ok = 'ok'
#                 c.save()
#
#         return HttpResponseRedirect('/pingjia/')
#
#
# # 学生已评价
# @check_login
# def ok_pingjia(request):
#     xuehao = request.session['xuehao']
#     tiku = TiKu_1.objects.filter(is_active=True)
#     book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no')  #
#     book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok').order_by('id')  #
#     return render(request, 'login/ok_pingjia.html', locals())
#
#
# # 学生查看已评价
# @check_login
# def cat_pingjia(request, kecheng_id):
#     xuehao = request.session['xuehao']
#     book = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='no')  #
#     book1 = KeCheng.objects.filter(xuehao=xuehao, is_active=True, ok='ok').order_by('id')  #
#
#     tiku = TiKu_1.objects.filter(is_active=True)
#     pingjia = PingJia.objects.get(id=kecheng_id)
#
#     return render(request, 'login/cat_pingjia.html', locals())


# 首页
def index(request):
    return render(request, 'index.html')


# 教师查看班级页面
# @check_login
# def teacher_index(request):
#     '''
#
#         1.教师id
#         2.班级过滤器
#         3.跳转到班级评价
#
#
#     '''
#     teacher_id = request.session['teacher_id']
#     a = KeCheng.objects.filter(teacher_id=teacher_id, is_active=True).values('xuehao__banji', 'xuehao', 'id')  # 学生班级
#     return render(request, 'teacher/index.html', locals())


# 教师查看班级评价页面
# @check_login
def teacher_pingjia(request, banji_id):
    """
    1.班级过滤器
    2.学生评价了
    3.学生评价平均值
    4.总评价
from django.db.models import Avg,Max,Min,Count,Sum

    """
    from django.db.models import Avg, Max, Min, Count, Sum
    teacher_id = request.session['teacher_id']
    pingjiabaio = PingJia.objects.filter(is_active=True,
                                         kecheng__xuehao__banji=banji_id,
                                         kecheng__teacher_id=teacher_id)  # 评价

    tiku = TiKu_1.objects.filter(is_active=True)  # 题库
    a = KeCheng.objects.filter(teacher_id=teacher_id, is_active=True) \
        .values('xuehao__banji', 'xuehao', 'id', 'ok')  # 班级过滤器
    b = KeCheng.objects.filter(teacher_id=teacher_id, is_active=True, xuehao__banji=banji_id)

    # 评价率  评价率 = 学生评价数  /  学生数
    pingjia_sum = KeCheng.objects.filter(is_active=True, xuehao__banji=banji_id, ok='ok').count()  # 学生评价书
    stu_sum = Students.objects.filter(is_active=True, banji=banji_id).count()
    PJL = float('%.2f' % (pingjia_sum / stu_sum * 100))

    # 求平均值
    avg = PingJia.objects.filter(kecheng__ok='ok',
                                 kecheng__teacher_id=teacher_id,
                                 kecheng__xuehao__banji=banji_id,
                                 ).aggregate(Avg("s_daan1"),
                                             Avg("s_daan2"),
                                             Avg("s_daan3"),
                                             Avg("s_daan4"),
                                             Avg("s_daan5"),
                                             Avg("s_daan6"),
                                             Avg("s_daan7"),
                                             Avg("s_daan8"),
                                             Avg("s_daan9"),
                                             Avg("s_daan10"))

    try:
        avg1 = float('%.2f' % avg['s_daan1__avg'])
        avg2 = float('%.2f' % avg['s_daan2__avg'])
        avg3 = float('%.2f' % avg['s_daan3__avg'])
        avg4 = float('%.2f' % avg['s_daan4__avg'])
        avg5 = float('%.2f' % avg['s_daan5__avg'])
        avg6 = float('%.2f' % avg['s_daan6__avg'])
        avg7 = float('%.2f' % avg['s_daan7__avg'])
        avg8 = float('%.2f' % avg['s_daan8__avg'])
        avg9 = float('%.2f' % avg['s_daan9__avg'])
        avg10 = float('%.2f' % avg['s_daan10__avg'])
        # 综合评价
        s = 0
        s2 = 0
        for i in avg:
            if avg[i] != 0:
                s += 1
                s2 += avg[i]
        s_avg = s2 / s
        s_avg = float('%.2f' % s_avg)
    except Exception as e:
        print('ok')

    return render(request, 'teacher/pingjia_ok.html', locals())


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
# @check_login
# def update_password(request):
#     if request.method == 'GET':
#
#         return render(request, 'pingjiaxitong/update_password.html')
#     elif request.method == 'POST':
#         xuehao = request.session['xuehao']
#         pswd = request.POST['password']
#         pswd_1 = request.POST['password_1']
#         pswd_2 = request.POST['password_2']
#
#         # 哈希算法
#         # m = hashlib.md5()
#         # m.update(pswd.encode())
#         # password_m = m.hexdigest()
#
#         # 原密码是否相同
#         if pswd_1 != pswd_2:
#             # return HttpResponse('密码不一致！！！')
#             msg = '密码不一致！！！'
#             return render(request, "pingjiaxitong/update_password.html", locals())
#         try:
#             s = Students.objects.filter(xuehao=xuehao, password=pswd_1)
#         except Exception as e:
#             return HttpResponse('报错', e)
#
#         # 哈希算法
#         # m = hashlib.md5()
#         # m.update(pswd_1.encode())
#         # password_m = m.hexdigest()
#         # 是否账号密码一样
#         if s:
#             # 如果是修改密码
#             s.update(password=pswd_1)
#             # 免登录一天
#             request.session['xuehao'] = xuehao
#
#             msg = '修改密码成功！'
#
#             return HttpResponseRedirect('/pingjia/', locals())
#         else:
#             msg = '密码错误！'
#             return render(request, 'pingjiaxitong/update_password.html', locals())


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

        return HttpResponse('注册成功！')

# # 管理员首页
# def myadmin(request):
#     """
#
#     1.教师管理页面
#         添加
#         删除
#         编辑
#         ————是否首页显示——————
#
#     2.学生管理页面
#         添加
#         删除
#         编辑
#     3.课程管理页面
#         添加
#         删除
#         编辑
#     4.管理评价
#         添加
#         删除
#         编辑
#     """
#
#     return render(request, 'guanliyuan/index.html', locals())
#
#
# # 管理学生页面
# def myadmin_stu(request, pIndex=1):
#     stu_list = Students.objects.filter(is_active=True)  # 班级过滤器
#     mywhere = []
#     # 获取并判断搜索
#     kw = request.GET.get("keyword", None)
#     if kw:
#         stu_list = stu_list.filter(Q(xuehao__contains=kw) | Q(name__contains=kw))
#         mywhere.append('keyword' + kw)
#
#     # 执行分页处理
#     pIndex = int(pIndex)
#     page = Paginator(stu_list, 10)  # 以每页9条数据分页
#     maxpagex = page.num_pages  # 获取最大页数
#     # 判断当前页是否越界
#     if pIndex > maxpagex:
#         pIndex = maxpagex
#     if pIndex < 1:
#         pIndex = 1
#
#     list2 = page.page(pIndex)  # 获取当前页数据
#     plist = page.page_range  # 获取页码表信息
#     context = {"stulist": list2, "plist": plist, "pIndex": pIndex, "max_pages": maxpagex, 'mywehere': mywhere}
#     return render(request, 'guanliyuan/myadmin_stu.html', context)
#
#
# # 添加学生
# def admin_stu_add(request):
#     if request.method == "GET":
#         return render(request, 'guanliyuan/admin_add.html')
#     if request.method == "POST":
#         xuehao = request.POST['xuehao']
#         name = request.POST['name']
#         phone = request.POST['phone']
#         banji = request.POST['banji']
#         return HttpResponse('ok')
#
#
# # 编辑学生信息
# def admin_stu_edit(request, xuehao_id):
#     return HttpResponse(xuehao_id)
#
#
# # 学生删除
# def admin_stu_del(request, xuehao_id):
#     return None
#
#
# # 上传学生信息
# def admin_stu_upload(request):
#     return None
#
#
# # 查看上传的的学生信息
# def admin_stu_toupload(request):
#     return None
