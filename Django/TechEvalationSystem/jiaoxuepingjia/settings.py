

import os
from pathlib import Path

from django.core import mail

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o&!rf2&kj3sjwwx6h8@dt%n7pla9agl2=-su0b=v36q$m^+tw2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
X_FRAME_OPTIONS = 'ALLOWALL'

# Application definition

INSTALLED_APPS = [
    #'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'login',
    'students',
    'teachers',
    'myadmin',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'login.SimpleMiddleware.SimpleMiddleware',  # 注册自定义中间件
]

ROOT_URLCONF = 'jiaoxuepingjia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'jiaoxuepingjia.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'pingjiao',
#         'USER': 'root',
#         'PASSWORD': 'Hm245938',
#         'HOST': '127.0.0.1',
#         'PORT': 3306,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR / 'static'), ]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 隐藏右侧SimpleUI广告链接和使用分析
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['学生管理', '教师管理', '课程管理', '调查卷管理', '评价管理', '管理员'],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'name': '学生管理',
        # 'icon': 'fas fa-code',
        'url': '/admin/login/students/'
    }, {
        'name': '教师管理',
        # 'icon': 'fas fa-code',
        'url': '/admin/login/kecheng/'
    }, {
        'name': '调查卷管理',
        # 'icon': 'fas fa-code',
        'url': '/admin/login/tiku_1/'
    }, {
        'name': '评价管理',
        'models': [{
            'name': '首页',
            'url': '/myadmin/'
        }, {
            'name': '评价成绩',
            'url': '/myadmin/pingjia/'
        }, {
            'name': '班级评价率',
            'url': '/myadmin/pingjia_pjl/'
        }, {
            'name': '未评价学生名单',
            'url': '/myadmin/pingjia_not/'
        }]
    },
        {
            'name': '管理员',
            'icon': 'fa fa-user',
            'url': 'auth/user/'
        }]
}
