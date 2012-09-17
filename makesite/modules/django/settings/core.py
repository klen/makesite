" Common settings for all project. "
from os import path as op, walk
import logging

from settings import SOURCE_DIR, PROJECT_DIR, PROJECT_NAME


SECRET_KEY = "RedefineME.%s" % PROJECT_NAME

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_master.sqlite',
                'USER': '',
                'PASSWORD': '',
                'TEST_CHARSET': 'utf8',
    }
}

# Caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_PREFIX': '_'.join((PROJECT_NAME, 'CORE'))
    }
}

# Base urls config
ROOT_URLCONF = 'main.urls'

# Media settigns
MEDIA_ROOT = op.join(PROJECT_DIR, 'media')
STATIC_ROOT = op.join(PROJECT_DIR, 'static')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Templates settings
TEMPLATE_DIRS = ()
for root, dirs, files in walk(SOURCE_DIR, followlinks=True):
    if 'templates' in dirs:
        TEMPLATE_DIRS += (op.join(root, 'templates'),)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
)

# Applications
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
)

# Base apps settings
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# Middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

# Localization
USE_I18N = True
MIDDLEWARE_CLASSES += ('django.middleware.locale.LocaleMiddleware',)
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)

# Debug
INTERNAL_IPS = ('127.0.0.1',)

# Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
logging.info("Core settings loaded.")
