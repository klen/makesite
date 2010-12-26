from settings.project import *

# TEST SETTINGS
# --------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'USER': '',
        'PASSWORD': '',
        'TEST_CHARSET': 'utf8',
    }}
CACHES['default']['KEY_PREFIX'] = '_'.join((PROJECT_NAME, 'TST'))
