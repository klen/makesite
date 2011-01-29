from settings import PROJECT_NAME
from settings.core import *


# PROJECT SETTINGS
# -----------------
INSTALLED_APPS += (

    # Community apps
    'south',

    # Base project app
    'main',

)

CACHES['default']['KEY_PREFIX'] = '_'.join((PROJECT_NAME, 'PRJ'))
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
