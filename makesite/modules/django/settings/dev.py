" Settings for dev zones. "
from settings.project import *
from settings.core import TEMPLATE_LOADERS

assert TEMPLATE_LOADERS

# Caches
CACHES['default']['KEY_PREFIX'] = '_'.join((PROJECT_NAME, 'DEV'))

# Debug
DEBUG = True
TEMPLATE_DEBUG = True
if DEBUG:
    INTERNAL_IPS += tuple('192.168.1.%s' % x for x in range(1, 111))
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware', )
    INSTALLED_APPS += ('debug_toolbar', )
    DEBUG_TOOLBAR_CONFIG = dict(INTERCEPT_REDIRECTS=False)

# pymode:lint_ignore=W404
