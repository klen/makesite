import logging
import sys
from argparse import ArgumentParser
from os import walk, path as op, listdir, access, X_OK, environ, pathsep
from initools.configparser import ConfigParser, Error
from subprocess import check_call
from sys import stdout
from tempfile import mktemp

from makesite.settings import CFGNAME, TPLNAME, TPL_DIR, MOD_DIR, VERSION


# Log settings
LOGGER = logging.getLogger('Makesite')
LOGGER.setLevel(logging.INFO)
LOGFILE_HANDLER = logging.FileHandler(mktemp())
LOGGER.addHandler(LOGFILE_HANDLER)
LOGGER.addHandler(logging.StreamHandler(stdout),)


ACTIONS = dict()


class MakesiteArgsParser(ArgumentParser):

    def error(self, message):
        self.print_usage(sys.stderr)
        print "\nInstalled templates:"
        print " ".join(get_base_templates())
        print "\nInstalled modules:"
        print " ".join(get_base_modules())
        print
        self.exit(2, '%s: error: %s\n' % (self.prog, message))


def action(*arguments):
    parser = MakesiteArgsParser(description="'Makesite' easy control of project structure.")
    parser.add_argument('-v', '--version', action='version', version=VERSION, help='Show makesite version')
    for (args, kwargs) in arguments:
        parser.add_argument(*args, **kwargs)

    def _inner(func):
        name = func.__name__
        parser.description = func.__doc__

        def _wrapper(args=None):
            args = parser.parse_args(args)
            return func(args)

        ACTIONS[name] = _wrapper
        if name != 'main':
            parser.prog = " ".join((parser.prog, name))
        return _wrapper

    return _inner


class OrderedSet(list):

    def __init__(self, sequence):
        result = []
        for o in sequence:
            if not o in result:
                result.append(o)
        super(OrderedSet, self).__init__(result)


class MakesiteException(AssertionError):
    " Exception raised by makesite "
    pass


class MakesiteParser(ConfigParser):

    def __init__(self, *args, **kwargs):
        super(MakesiteParser, self).__init__(*args, **kwargs)
        self.add_section('Main')
        self.add_section('Templates')

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
        " Return template context. "
        items = super(MakesiteParser, self).items(section, **kwargs)
        return dict(items)

    def read(self, filenames, extending=False, map_sections=None):
        if isinstance(filenames, basestring):
            filenames = [filenames]
        filenames = filter(op.exists, filenames)
        if not filenames:
            return False
        LOGGER.info("Read params: %s" % filenames)
        return super(MakesiteParser, self).read(filenames, extending=extending, map_sections=map_sections)


def get_project_templates(path):
    " Get list of installed templates. "

    try:
        return open(op.join(path, TPLNAME)).read().strip().split(',')
    except IOError:
        raise MakesiteException("Invalid makesite-project: %s" % path)


def get_base_modules():
    " Get list of installed modules. "

    return sorted(filter(
            lambda x: op.isdir(op.join(MOD_DIR, x)),
            listdir(MOD_DIR)))


def get_base_templates():
    " Get list of installed templates. "

    return sorted(filter(
            lambda x: op.isdir(op.join(TPL_DIR, x)),
            listdir(TPL_DIR)))


def print_header(msg, sep='='):
    " More strong message "

    LOGGER.info("\n%s\n%s" % (msg, ''.join(sep for _ in msg)))


def which(program):
    " Check program is exists. "

    head, _ = op.split(program)

    if head:
        if is_exe(program):
            return program
    else:
        for path in environ["PATH"].split(pathsep):
            exe_file = op.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def call(cmd, shell=True, **kwargs):
    " Run shell command. "

    LOGGER.info("Cmd: %s" % cmd)
    check_call(cmd, shell=shell, stdout=LOGFILE_HANDLER.stream, **kwargs)


def walklevel(dirpath, level=1):
    dirpath = dirpath.rstrip(op.sep)
    assert op.isdir(dirpath)
    start = dirpath.count(op.sep)
    for root, dirs, files in walk(dirpath):
        yield root, dirs, files
        if start + level <= root.count(op.sep):
            del dirs[:]


def is_exe(path):
    return op.exists(path) and access(path, X_OK)


def gen_template_files(path):
    " Generate relative template pathes. "

    path = path.rstrip(op.sep)
    for root, _, files in walk(path):
        for f in filter(lambda x: not x in (TPLNAME, CFGNAME), files):
            yield op.relpath(op.join(root, f), path)
