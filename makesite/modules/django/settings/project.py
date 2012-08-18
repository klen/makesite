" Settings for production. "
from settings import PROJECT_NAME
from settings.core import *

# Applications
INSTALLED_APPS += (

    # Community apps
    'south',

    # Base project app
    'main',

)

# Caches
CACHES['default']['KEY_PREFIX'] = '_'.join((PROJECT_NAME, 'PRJ'))

# Sessions
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Templates cache
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
)

# pymode:lint_ignore=W404
