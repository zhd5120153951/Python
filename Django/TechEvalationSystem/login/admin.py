from django.contrib import admin

from .models import *

admin.site.site_title = "评价管理后台系统"

admin.site.site_header = "评价系统后台管理"

admin.site.index_title = "后台管理"


class GuanLiYuanManager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['name', 'password', 'is_active']


class StudentsManager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['xuehao', 'name', 'sex', 'email', 'phone', 'is_active']


# 控制list_display中的字段可以链接到修改页
# list_display_links = ['id']
# 过滤器
# list_filter = ['zhuti']
# 添加搜索框[模糊查询]
# search_fields = ['neirong']
# 添加可在列表页编辑的字段
# list_editable = ['price']


class TeachersManager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['teacher_id', 'name', 'sex', 'email', 'phone', 'is_active']


class TiKu_1Manager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['id', 'timu', 'is_active']


class PingJiaManager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['id', 'kecheng', 's_liuyan']


class KeChengManager(admin.ModelAdmin):
    # 列表页显示那些字段
    list_display = ['id', 'kecheng', 'xuehao', 'teacher_id', 'ok']
    # 添加可在列表页编辑的字段
    list_editable = ['ok']


admin.site.register(GuanLiYuan, GuanLiYuanManager)
admin.site.register(Students, StudentsManager)
admin.site.register(Teachers, TeachersManager)
admin.site.register(TiKu_1, TiKu_1Manager)
admin.site.register(PingJia, PingJiaManager)
admin.site.register(KeCheng, KeChengManager)
