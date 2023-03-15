import datetime
import os
from pathlib import Path
from django.conf import global_settings

"""
    配置文件
"""

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-g3tbq-r39yts4gra0ukj5#^df*(i!d(#()is#rtv8i8=5fvnh%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.159.128', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.userapp',
    'apps.newsapp',
    'apps.verifications',   # 异步服务
    'apps.oauth',           # QQ登陆接口应用
    'apps.payment',         # 支付宝接口应用
    'haystack',             # 全文检索
    'django_crontab',       # 定时任务
    'corsheaders',          # 跨域访问
    'apps.mg_admin',        # 后台项目应用
    'rest_framework',       # drf

]
# Application definition


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 一定要放到第一行 配置中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'portey_road.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.newsapp.mycontext.get_channels',
                'apps.newsapp.mycontext.get_comment',
            ],
            # 导入jinja2环境
            'environment': 'utils.jinja2_env.environment'
        },
    }
]

WSGI_APPLICATION = 'portey_road.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mango',
        'USER': 'zsb',
        'PASSWORD': '987563sb',
        'HOST': '192.168.159.128',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

# 当这个参数为True时
# 保证存储到数据库中的是 UTC 时间；
# 在函数之间传递时间参数时，确保时间已经转换成 UTC 时间
# 为False后在想使用utc时间 下面格式 但如果配置中时区不是UTC 就按原来的写就行
import datetime
from django.utils.timezone import utc
utcnow = datetime.datetime.utcnow().replace(tzinfo=utc)
USE_TZ = True
# USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 配置Redis数据库
CACHES = {
    # 默认
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # session
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 验证码
    "verify_code": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# 配置项⽬⽇志
LOGGING = {
    'version': 1,
    # 是否禁⽤已经存在的⽇志器
    'disable_existing_loggers': False,
    # ⽇志信息显示的格式
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # 对⽇志进⾏过滤
    'filters': {
        # django在debug模式下才输出⽇志
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # ⽇志处理⽅法
        'console': {  # 向终端中输出⽇志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        # 向⽂件中输出⽇志
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/mango.log',
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # ⽇志器
        'django': {  # 定义了⼀个名为django的⽇志器
            'handlers': ['console', 'file'],  # 可以同时向终端与⽂件中输出⽇志
            'propagate': True,  # 是否继续传递⽇志信息
            'level': 'INFO',  # ⽇志器接收的最低⽇志级别
        },
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 添加apps目录的运行环境 避免apps目录下的所有app不能被django识别
# 并将框架自带的user重写 应用名.对应的用户模型
import sys

sys.path.insert(0, str(BASE_DIR / 'apps'))
AUTH_USER_MODEL = 'userapp.Users'

# global_settings


# 配置短信验证码参数 互亿无线
APIID = 'C65298723'
APIKEY = '0e897cbb115369e909125983f84874ce'

# 第三方QQ登录配置参数
QQ_CLIENT_ID = ''
QQ_APP_KEY = ''
QQ_REDIRECT_URI = ''

# 支付宝配置
ALIPAY_APPID = '2021000119603533'
ALIPAY_DEBUG = True
ALIPAY_URL = 'https://openapi.alipaydev.com/gateway.do/'  # 网关接口
ALIPAY_RETURN_URL = 'http://127.0.0.1:8000/payment/status/'  # 自己定义的支付成功的页面url

# 指定自定义类路径 让整个项目识别
AUTHENTICATION_BACKENDS = ['apps.userapp.auth.MultiAccountLoginAuth']

# 指定登录首页请求地址 一般是用于判断用户是否登录然后重定向到指定的页面
LOGIN_URL = '/login/'

# 配置文件下载的前缀 http:// + 服务器ip + 端口号(nginx的默认端口号是8888)
FDFS_BASE_URL = 'http://192.168.159.128:8888/'

# 指定管理员用户上传图片的地址
FASTDFS_CONFIG_PATH = os.path.join(BASE_DIR, 'utils/fastdfs/client.conf')

# 配置项目的文件存储系统
DEFAULT_FILE_STORAGE = 'utils.fastdfs.fdfs_storage.FastDFSStorage'

# 配置Haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://192.168.159.128:9200',  # elasticsearch的服务器ip和端口号(默认9200)
        'INDEX_NAME': 'mango_indexes',  # elasticsearch建立的索引库名称
    },
}

# 当增改删时 自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 设置搜索结果每页显示的记录数
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 4

# 定时任务配置
CRONJOBS = [
    #  每分钟生成一次首页静态文件
    #   *   *    *   *   *
    #   分   时   日   月  周
    #   分也可用 */1表示 每几分钟
    ('*/1 * * * * ', 'apps.newsapp.static_index.static_index', '>' + os.path.join(BASE_DIR, 'logs/crontab.log'))
]
# 解决crontab的中文问题
CRONTAB_COMMAND_PREFIX = 'LANG_ALL=zh_cn.UTF-8'

# 设置CORS⽩名单 凡是出现在白名单的都可以访问后端接口 即前段运行时的ip port
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://0.0.0.0:8080',
    'http://0.0.0.0:8000',

)
CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# drf配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'apps.mg_admin.utils.PageNumPagination',


}

# JWT配置
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 'JWT_ALLOW_REFRESH': True,
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'apps.mg_admin.utils.jwt_response_payload_handler',
}

