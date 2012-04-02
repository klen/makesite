from os import path as op, environ, getenv


VERSION = '0.9.41'

BASEDIR = op.abspath(op.dirname(__file__))
TPL_DIR = op.join(BASEDIR, 'templates')
MOD_DIR = op.join(BASEDIR, 'modules')

TPLNAME = '.makesite'
CFGNAME = 'makesite.ini'

BASECONFIG = op.join(BASEDIR, CFGNAME)
HOMECONFIG = op.join(getenv('HOME', '~'), CFGNAME)

MAKESITE_HOME = environ.get('MAKESITE_HOME')

SRC_CLONE = (
    ('svn', 'svn checkout %(src)s %(source_dir)s'),
    ('git', 'git clone %(src)s %(source_dir)s -b %(branch)s'),
    ('hg',  'hg clone %(src)s %(source_dir)s'),
)
