import hashlib

from django.shortcuts import render

from login.models import *


# Create your views here.
# def check_login(fn):
#     def wrap(request, *args, **kwargs):
#         status = request.session.get('teacher_id')
#         if not status:  # 报错
#             s_xuehao = request.COOKIES.get('teacher_id')
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
#                 request.session['teacher_id'] = s_xuehao
#
#         return fn(request, *args, **kwargs)
#
#     return wrap

# @check_login
def teacher_index(request):
    '''

        1.教师id
        2.班级过滤器
        3.跳转到班级评价


    '''
    teacher_id = request.session['teacher_id']
    a = KeCheng.objects.filter(teacher_id=teacher_id, is_active=True).values('xuehao__banji', 'xuehao', 'id')  # 学生班级
    return render(request, 'teachers/index.html', locals())


# @check_login
"""
    1.班级过滤器
    2.学生评价了
    3.学生评价平均值
    4.总评价
    from django.db.models import Avg,Max,Min,Count,Sum

"""


def teacher_pingjia(request, banji_id):
    from django.db.models import Avg
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

    return render(request, 'teachers/pingjia_ok.html', locals())


def pswd_update(request):
    if request.method == 'GET':
        return render(request, 'teachers/pswd_updat.html')
    if request.method == 'POST':
        name = request.session.get('teacher_id')
        pswd = request.POST['pswd']
        pswd_1 = request.POST['pswd_1']
        pswd_2 = request.POST['pswd_2']

        # 哈希算法
        m = hashlib.md5()
        m.update(pswd.encode())
        password_m = m.hexdigest()

        if pswd_1 != pswd_2:
            msg = "新密码不一致！！！"
            return render(request, 'teachers/pswd_updat.html', {"msg": msg})
        try:
            ss = Teachers.objects.filter(teacher_id=name, password=password_m, is_active=True)
            sm = Teachers.objects.get(teacher_id=name, is_active=True)
        except Exception as e:
            print("teacher_update_pswd:", e)
        if ss:
            # 哈希算法
            m = hashlib.md5()
            m.update(pswd_1.encode())
            password_m = m.hexdigest()
            sm.password = password_m
            sm.save()
            msg = "密码修改成功！！"
            return render(request, 'index.html', {"msg": msg})
        else:
            msg = "原密码错误！"
            return render(request, 'teachers/pswd_updat.html', {"msg": msg})
