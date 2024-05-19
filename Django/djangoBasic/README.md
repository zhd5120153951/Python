djangoBasic
    |—— manage.py
    |__ djangoBasic
        |—— __init__.py
        |—— settings.py(项目配置文件，比如链接那个数据)
        |—— urls.py (跟路由，URL和函数对应关系，/x1/login  -->  do_login)
        |—— asgi.py (异步运行，编写socket处理web请求)
        |—— wsgi.py (同步运行，编写socket处理web请求)
    |__ Greatech(网站，主应用)
        |—— migrations
            |__ __init__.py
        |—— __init__.py
        |—— admin.py (内部后台管理的配置，不要动)
        |—— apps.py (App名字，不要动)
        |—— models.py (数据库，类-->SQL语句(ORM映射)，就是自己不用写SQL语句了)--常用
        |—— tests.py (单元测试，不要轻易动)
        |—— views.py (视图函数，实现的urls.py中的请求的接口的业务逻辑函数)--常用
    |__ AI(子应用--同主应用一样)
补充1：Django框架中添加多个app时，templates和static要放在每个app内，外面的放公共的资源，启动项目时：资源搜索路径是先在最外层路径找templates和static，找不到后再去对应的app文件夹下的templates和static中找
补充2：数据库默认是sqlite,可以改为MySQL
补充3：Django的项目创建流程:
        1.终端中激活虚拟环境，django-admin startproject "项目名"
        2.python manage.py startup "app名字"
        3.注册app，在settings.py中的installed_apps中加入"app名字.apps.app名字Config"
        4.数据库更换或者不更换