from django.db import models


# 评价系统管理员
# Create your models here.
class GuanLiYuan(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32, primary_key=True)  # 管理员用户名
    password = models.CharField(verbose_name="密码", max_length=32)  # 管理员密码
    email = models.EmailField(verbose_name="邮箱", default='')
    phone = models.CharField(verbose_name="手机号", max_length=11, default='')
    zhiwu = models.CharField(verbose_name="职务", max_length=28, default='')
    photo = models.ImageField(verbose_name="头像", upload_to='admin/', default='')
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.name

    class Meta:
        # 数据库列表名
        db_table = 'GuanLiYuan'
        # admin后台管理名
        verbose_name_plural = '管理员列表'


# 评价题库模型
class TiKu_1(models.Model):
    id = models.IntegerField(verbose_name="ID", primary_key=True)  # id
    timu = models.TextField(verbose_name="题目", max_length=210, default='')  # 评价题目

    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.timu

    class Meta:
        # 数据库列表名
        db_table = 'TiKu_1'
        # admin后台管理名
        verbose_name_plural = '题库'


# 学生模型
class Students(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=28, default='')
    password = models.CharField(verbose_name="密码", max_length=60, default='')
    xueyuan = models.CharField(verbose_name="学院", max_length=28, default='')
    banji = models.CharField(verbose_name="班级", max_length=28, default='')
    xuehao = models.CharField(verbose_name="学号", max_length=12, default='', primary_key=True)  # unique=True
    sex = models.CharField(verbose_name='性别', max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    email = models.EmailField(verbose_name="邮箱", default='')
    phone = models.CharField(verbose_name="手机号", max_length=11, default='')
    photo = models.ImageField(verbose_name="头像", upload_to='Students/', default='')
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.xuehao

    # return '%s_%s_%s_%s_%s_%s' % (self.name, self.banji, self.xuehao, self.sex,self.email,self.phone)

    class Meta:
        # 数据库列表名
        db_table = 'Students'
        # admin后台管理名
        verbose_name_plural = '学生列表'


# 教师模型
class Teachers(models.Model):
    # id = models.CharField("id", max_length=12, primary_key=True)
    name = models.CharField(verbose_name="姓名", max_length=28, default='')
    password = models.CharField(verbose_name="密码", max_length=60, default='')
    teacher_id = models.CharField(verbose_name="教师id", max_length=12, primary_key=True, default='')  # primary_key=True
    sex = models.CharField(verbose_name='性别', max_length=6, choices=(('male', '男'), ('female', '女')), default='male')
    email = models.EmailField(verbose_name="邮箱", default='')
    phone = models.CharField(verbose_name="手机号", max_length=11, default='')
    photo = models.ImageField(verbose_name="头像", upload_to='teacher/', default='')
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return '%s-%s-%s-%s' % (self.teacher_id, self.name, self.sex, self.phone)

    class Meta:
        # 数据库列表名
        db_table = 'Teachers'
        # admin后台管理名
        verbose_name_plural = '教师列表'


# 评价模型
class PingJia(models.Model):
    id = models.CharField(verbose_name="id", max_length=11, primary_key=True, default='')
    kecheng = models.OneToOneField(to="KeCheng", on_delete=models.CASCADE, verbose_name="课程", default='')
    s_daan1 = models.DecimalField(verbose_name="学生答案1", max_digits=5, decimal_places=2, default=0)
    s_daan2 = models.DecimalField(verbose_name="学生答案2", max_digits=5, decimal_places=2, default=0)
    s_daan3 = models.DecimalField(verbose_name="学生答案3", max_digits=5, decimal_places=2, default=0)
    s_daan4 = models.DecimalField(verbose_name="学生答案4", max_digits=5, decimal_places=2, default=0)
    s_daan5 = models.DecimalField(verbose_name="学生答案5", max_digits=5, decimal_places=2, default=0)
    s_daan6 = models.DecimalField(verbose_name="学生答案6", max_digits=5, decimal_places=2, default=0)
    s_daan7 = models.DecimalField(verbose_name="学生答案7", max_digits=5, decimal_places=2, default=0)
    s_daan8 = models.DecimalField(verbose_name="学生答案8", max_digits=5, decimal_places=2, default=0)
    s_daan9 = models.DecimalField(verbose_name="学生答案9", max_digits=5, decimal_places=2, default=0)
    s_daan10 = models.DecimalField(verbose_name="学生答案10", max_digits=5, decimal_places=2, default=0)
    s_avg = models.DecimalField(verbose_name="平均成绩", max_digits=5, decimal_places=2, default=0)

    s_liuyan = models.TextField(verbose_name="学生留言", default='', max_length=210, null=True)
    is_active = models.BooleanField('是否活跃', default=True)

    # def __str__(self):
    #     return self.kecheng

    class Meta:
        # 数据库列表名
        db_table = 'PingJia'
        # admin后台管理名
        verbose_name_plural = '评价表'


# # 课表
# class Kebiao(models.Model):
#     id = models.CharField(verbose_name="id", primary_key=True, max_length=60)
#     class_name = models.CharField(verbose_name="课程名", max_length=128, default='')
#
#     def __str__(self):
#         return self.id
#
#     class Meta:
#         # 数据库列表名
#         db_table = 'Kebiao'
#         # admin后台管理名
#         verbose_name_plural = '课表'


# 选课表
class KeCheng(models.Model):
    id = models.CharField(verbose_name="id", primary_key=True, max_length=11, default='')
    # xueqi = models.ForeignKey(to="XueQi", on_delete=models.CASCADE, verbose_name="学期", default='')
    # kecheng = models.ForeignKey(to="KeBiao", on_delete=models.CASCADE, verbose_name="选课表", default='')
    kecheng = models.CharField(verbose_name="课表", max_length=128, default='')
    xuehao = models.ForeignKey(to="Students", on_delete=models.CASCADE, verbose_name="学号", default='')
    teacher_id = models.ForeignKey(to="Teachers", on_delete=models.CASCADE, verbose_name="教工号", default='')
    ok = models.CharField(verbose_name='是否已评价', max_length=6, choices=(('ok', '是'), ('no', '否')), default='no')
    is_active = models.BooleanField('是否活跃', default=True)

    def __str__(self):
        return self.kecheng

    class Meta:
        # 数据库列表名
        db_table = 'Kecheng'
        # admin后台管理名
        verbose_name_plural = '选课表'

# # 学期模型
# class XueQi(models.Model):
#     xuenian = models.CharField(verbose_name="学年", max_length=20, default='')
#     xueqi = models.CharField(verbose_name="学期", max_length=20, default='')
#     is_active = models.BooleanField('是否活跃', default=True)
#
#     def __str__(self):
#         return self.xuenian
#
#     class Meta:
#         # 数据库列表名
#         db_table = 'XueQiBiao'
#         # admin后台管理名
#         verbose_name_plural = '学期列表'
