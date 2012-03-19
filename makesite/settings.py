from os import path as op, environ, getenv


VERSION = '0.9.31'

BASEDIR = op.abspath(op.dirname(__file__))
TPL_DIR = op.join(BASEDIR, 'templates')
MOD_DIR = op.join(BASEDIR, 'modules')

TPLNAME = '.makesite'
CFGNAME = 'makesite.ini'

BASECONFIG = op.join(BASEDIR, CFGNAME)
HOMECONFIG = op.join(getenv('HOME', '~'), CFGNAME)

MAKESITE_HOME = environ.get('MAKESITE_HOME')

SRC_CLONE = (
    ('svn', 'svn checkout %s %s'),
    ('git', 'git clone %s %s'),
    ('hg',  'hg clone %s %s'),
)
