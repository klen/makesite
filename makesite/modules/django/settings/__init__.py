import os.path


PROJECT_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../'))
DEVZONE_ROOT = os.path.realpath(os.path.join(PROJECT_ROOT, '../'))
DB_FILE = os.path.join(PROJECT_ROOT, '.db')
CONFIG_FILE = os.path.join(DEVZONE_ROOT, '.project.ini')


# Load configs from project ini file (sitegen generated)
if os.path.exists(CONFIG_FILE):
    import ConfigParser
    parser = ConfigParser.RawConfigParser()
    parser.read(CONFIG_FILE)
    V = dict(parser.items('Main'))

else:
    V = dict()


PROJECT_NAME = "%s.%s" % (V.get('project', 'undefined'), V.get('branch', 'master'))
__TEMPLATES = V.get('template', '').split()


def parse_db():
    """ Load databases from .db file.
    """
    if not os.path.exists(DB_FILE):
        return None

    databases = dict()
    for line in open( DB_FILE ).readlines():
        if line.startswith('#') or not len(line.strip()):
            continue
        name, backend, connect_data = line.split()
        user_data, db_data = connect_data.split('@')
        user, password = user_data.split(':')
        host, db_name = db_data.split('/')
        databases[ name ] = dict(
                ENGINE = backend,
                NAME = db_name,
                HOST = host,
                USER = user,
                PASSWORD = password,
        )
    return databases


def parse_cache():
    """ Parse cache from makesite templates.
    """
    caches = dict(default=dict(KEY_PREFIX = '_'.join((PROJECT_NAME, 'CORE'))))

    if 'memcached' in __TEMPLATES:
        caches['default']['BACKEND'] = 'django.core.cache.backends.memcached.MemcachedCache'
        caches['default']['LOCATION'] = ':'.join((V.get('memcached_host', 'localhost'), V.get('memcached_port', '11211')))

    else:
        caches['default']['BACKEND'] = 'django.core.cache.backends.locmem.LocMemCache'

    return caches
