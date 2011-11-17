from os import path, environ, getenv


VERSION = '0.9.12'

BASEDIR = path.abspath(path.dirname(__file__))
TPL_DIR = path.join(BASEDIR, 'templates')
MOD_DIR = path.join(BASEDIR, 'modules')

TPLNAME = '.makesite'
CFGNAME = 'makesite.ini'

BASECONFIG = path.join(BASEDIR, CFGNAME)
HOMECONFIG = path.join(getenv('HOME', '~'), CFGNAME)

MAKESITE_HOME = environ.get('MAKESITE_HOME')

SRC_TYPES = (
    ('svn', '%s checkout %s %s'),
    ('git', '%s clone %s %s'),
    ('hg', '%s clone %s %s'),
)
