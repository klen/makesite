from os import path as op, environ, getenv

from initools.configparser import ConfigParser, Error


BASEDIR = op.abspath(op.dirname(__file__))
TPL_DIR = op.join(BASEDIR, 'templates')
MOD_DIR = op.join(BASEDIR, 'modules')

TPLNAME = '.makesite'
CFGNAME = 'makesite.ini'

BASECONFIG = op.join(BASEDIR, CFGNAME)
HOMECONFIG = op.join(getenv('HOME', '~'), CFGNAME)

MAKESITE_HOME = environ.get('MAKESITE_HOME')
USER = environ.get('USER', 'roor')

SRC_CLONE = (
    ('svn', 'svn checkout %(src)s %(source_dir)s'),
    ('git', 'git clone %(src)s %(source_dir)s -b %(branch)s'),
    ('hg', 'hg clone %(src)s %(source_dir)s'),
)


class MakesiteParser(ConfigParser):

    def __init__(self, *args, **kwargs):
        super(MakesiteParser, self).__init__(*args, **kwargs)
        self.add_section('Main')
        self.add_section('Templates')
        self.add_section('alias')

    def defaults(self):
        return dict(self.items('Main'))

    def __getitem__(self, name):
        try:
            return self.get('Main', name)
        except Error:
            return None

    def __setitem__(self, name, value, section='Main'):
        self.set(section, name, value)

    def __getattr__(self, name):
        return self[name]

    def as_dict(self, section='Main', **kwargs):
        """Return template context from configs.

        """
        items = super(MakesiteParser, self).items(section, **kwargs)
        return dict(items)

    def read(self, filenames, extending=False, map_sections=None):
        if isinstance(filenames, basestring):
            filenames = [filenames]
        filenames = filter(op.exists, filenames)
        if not filenames:
            return False
        try:
            return super(MakesiteParser, self).read(filenames, extending=extending, map_sections=map_sections)
        except Exception:
            return False
