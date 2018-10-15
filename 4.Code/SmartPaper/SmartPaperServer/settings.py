#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g^4)=h@ir_n!azd^wsc-+p6*@12uvsjd%d4lzyv_egwyj^$hi_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH=False

ALLOWED_HOSTS = ['*']


# Application definition
# pip install django-cors-headers
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'SmartPaper',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# X_FRAME_OPTIONS = 'ALLOW-FROM *'

ROOT_URLCONF = 'SmartPaperServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['Front'],
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

WSGI_APPLICATION = 'SmartPaperServer.wsgi.application'

from SmartPaper.BaseMoudle.DBModule.DBHelper import *
# DATABASES = DBHelper.getDbConfig()

from SmartPaper.BaseMoudle.Logger.LoggerHelper import *
LoggerHandle = LoggerHelper.loadLoggerSetting(BASE_DIR)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cfppaper',
        'USER': 'root',
        'PASSWORD': '123456',
        # 'HOST':'192.168.1.209',
        'HOST':'127.0.0.1',
        'PORT': '3306',
        # 'OPTIONS':{
        #         "init_command":"SET foreign_key_checks = 0;",
        #     }
    }
}

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# HERE = os.path.dirname(os.path.dirname(__file__))
# MEDIA_ROOT = os.path.join(HERE, 'static/').replace('\\', '/')
# MEDIA_URL = '/static/'


# STATIC_ROOT 表示资源的根目录路径
# STATIC_URL 表示资源的访问url
# STATICFILES_DIRS 表示子资源的访问url和目录

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'SmartPaper')
STATIC_ROOT = os.path.join(STATIC_ROOT, 'static')

STATIC_TMP = os.path.join(BASE_DIR, 'SmartPaper')
STATIC_TMP = os.path.join(STATIC_TMP, 'templates')

print("========>" + STATIC_ROOT)

SRC_TEMPLATE = os.path.join(BASE_DIR, 'SmartPaper') #"D:\Work\Server\AdProject\SmartPaper\AdTemplate"
SRC_TEMPLATE = os.path.join(SRC_TEMPLATE, 'AdTemplate') #"D:\Work\Server\AdProject\SmartPaper\AdTemplate"

TempDir = os.path.join(os.getcwd(), 'SmartPaper')
TempDir2 = os.path.join(STATIC_ROOT, 'Service')
TempDir2 = os.path.join(TempDir, 'PreView')
TEMPLATE_DIRS = [os.path.join(TempDir, 'templates'),TempDir2]
print "TEMPLATE_DIRS",TEMPLATE_DIRS
# STATICFILES_DIRS = (
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     os.path.join(HERE,'static').replace('\\','/'),
# )
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "Front/static"),
]

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = 995
# EMAIL_HOST_USER = '609853524@qq.com'
# EMAIL_HOST_PASSWORD = 'caojj_123'
# DEFAULT_FROM_EMAIL = '609853524@qq.com'

#邮件配置
EMAIL_HOST = 'smtp.qq.com'                   #SMTP地址
EMAIL_PORT = 465                               #SMTP端口
EMAIL_HOST_USER = '609853524@qq.com'        #我自己的邮箱
EMAIL_HOST_PASSWORD = 'caojj_123'            #我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[Test Mail]'        #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                           #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#管理员站点
SERVER_EMAIL = '609853524@qq.com'       #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.


SYSTEM_CMDS={}

# Login
SYSTEM_CMDS["NORMAL_LOGIN"]          =      "账户通过Web登陆"
SYSTEM_CMDS["TERMINAL_LOGIN"]        =      "设备登陆"
SYSTEM_CMDS["HEART_BEAT"]            =      "心跳消息"
SYSTEM_CMDS["PSWD_RESET"]            =      "密码重置"
SYSTEM_CMDS["SET_USER_PSWD"]         =      "用户密码修改"

# Privilege
SYSTEM_CMDS["ORG_REGISTER"]          =      "添加单位"
SYSTEM_CMDS["ORG_MODI"]              =      "修改单位"
SYSTEM_CMDS["ORG_UNREGISTER"]        =      "删除单位"
SYSTEM_CMDS["LIST_ORGS"]             =      "列表单位数据"
SYSTEM_CMDS["QUERY_ORG"]             =      "查询单位详情"
SYSTEM_CMDS["GET_ORG_TREE"]          =      "获取单位树"
SYSTEM_CMDS["SET_ORG_SCREEN"]        =      "设置单位场景图"
SYSTEM_CMDS["ORG_ADD_ORG"]           =      "添加子单位"
SYSTEM_CMDS["ORG_MODI_ORG"]          =      "修改子单位"
SYSTEM_CMDS["ROLE_ADD"]              =      "添加角色"
SYSTEM_CMDS["ROLE_MODI"]             =      "修改角色"
SYSTEM_CMDS["ROLE_DELE"]             =      "删除角色"
SYSTEM_CMDS["ROLE_SET"]              =      "角色设置"
SYSTEM_CMDS["SET_USER_ROLES"]        =      "设置账户角色"
SYSTEM_CMDS["ROLE_LIST_USERS"]       =      "查询角色账户"
SYSTEM_CMDS["USERS_LIST_ROLES"]      =      "查询账户角色信息"
SYSTEM_CMDS["ROLE_QUERY"]            =      "角色查询"
SYSTEM_CMDS["ACCOUNT_LIST"]          =      "查询账户列表"
SYSTEM_CMDS["ACCOUNT_ADD"]           =      "添加账户"
SYSTEM_CMDS["ACCOUNT_DELE"]          =      "删除账户"
SYSTEM_CMDS["ACCOUNT_QUERY"]         =      "查询账户详情"
SYSTEM_CMDS["ACCOUNT_MODI"]          =      "修改账户"

# Device
SYSTEM_CMDS["LED_REGISTER"]         =      "LED注册"
SYSTEM_CMDS["LED_EDIT"]             =      "LED编辑"
SYSTEM_CMDS["LIGHT_REGISTER"]       =      "灯光注册"
SYSTEM_CMDS["LIGHT_EDIT"]           =      "编辑灯光"
SYSTEM_CMDS["DEVICE_EDIT"]          =      "设备编辑"
SYSTEM_CMDS["SET_DEVICE"]           =      "设置设备"
SYSTEM_CMDS["DEVICES_LIST"]         =      "列表设备"
SYSTEM_CMDS["DEVICE_INFO"]          =      "设备信息查询"
SYSTEM_CMDS["DEVICE_CONTROL"]       =      "设备控制"
SYSTEM_CMDS["SET_DEV_POSITION"]     =      "设置设备点位"
SYSTEM_CMDS["SET_DEV_POWER"]        =      "设置智能电源"
SYSTEM_CMDS["DEVICES_STAT"]         =      "设备统计"


# Power
SYSTEM_CMDS["POWER_ADD"]            =      "添加电源"
SYSTEM_CMDS["POWER_EDIT"]            =      "电源编辑"
SYSTEM_CMDS["POWER_SET"]            =      "设置电源"
SYSTEM_CMDS["POWERS_LIST"]          =      "电源列表"
SYSTEM_CMDS["POWER_INFO"]           =      "电源详情"
SYSTEM_CMDS["POWER_CONTROL"]        =      "电源控制"
SYSTEM_CMDS["POWER_QUERY_DEVS"]        =      "查询设备数据"

# Group
SYSTEM_CMDS["GROUP_ADD"]            =      "添加分区"
SYSTEM_CMDS["GROUP_DELE"]            =      "分区编辑"

SYSTEM_CMDS["GROUP_DELE"]           =      "删除分区"
SYSTEM_CMDS["GROUPS_LIST"]          =      "列表分区"
SYSTEM_CMDS["GROUP_INFO"]           =      "分区详情"
SYSTEM_CMDS["GROUP_CONFIG"]         =      "配置分区设备"
SYSTEM_CMDS["DEVS_MYGROUP"]         =      "分区设备检索"
SYSTEM_CMDS["GROUP_CLOSE_LIGHT"]         =      "关闭分区灯光"
SYSTEM_CMDS["GROUP_OPEN_LIGHT"]         =      "开启分区灯光"


# System
SYSTEM_CMDS["PARAM_SETTING"]         =      "设置系统参数"
SYSTEM_CMDS["SYSTEMCONFIG_LIST"]     =      "查询系统配置信息"
SYSTEM_CMDS["LOG_QUERY"]             =      "日志查询"
SYSTEM_CMDS["GET_DATAS"]             =      "元数据提取"
SYSTEM_CMDS["HOME_STAT"]             =      "首页数据统计"

# 策略
SYSTEM_CMDS["STRATEGYS_LIST"]            =      "策列列表"
SYSTEM_CMDS["STRATEGYS_ADD"]            =      "添加策略"
SYSTEM_CMDS["STRATEGYS_EDIT"]           =      "编辑策略"
SYSTEM_CMDS["STRATEGYS_INFO"]          =      "查询策略信息"
SYSTEM_CMDS["STRATEGYS_BIND"]           =      "策略绑定设备"
SYSTEM_CMDS["STRATEGYS_SET"]         =      "设置策略"
SYSTEM_CMDS["STRATEGYS_DEV_QUERY"]         =      "查询策略关联的设备"

SYSTEM_CMDS["VERSION_LIST"] = "版本查询"

