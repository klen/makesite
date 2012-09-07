import logging
import sys
from argparse import ArgumentParser
from datetime import datetime
from os import walk, path as op, listdir, access, X_OK, environ, pathsep
from subprocess import check_call
from sys import stdout
from tempfile import mktemp

from .settings import CFGNAME, TPLNAME, TPL_DIR, MOD_DIR
from makesite import version, terminal


LOGGER = logging.getLogger('Makesite')
LOGGER.setLevel(logging.INFO)
LOGFILE_HANDLER = logging.FileHandler(
    mktemp('.log', 'ms.%s-' % datetime.now().strftime('%d.%m')))
LOGGER.addHandler(LOGFILE_HANDLER)


class ColoredFormater(logging.Formatter):
    def format(self, record):
        s = logging.Formatter.format(self, record)
        if record.levelno == logging.DEBUG:
            return terminal.italic(s)
        if record.levelno == logging.INFO:
            return terminal.bold(s)
        if record.levelno == logging.WARN:
            return terminal.styled_text(
                "[WARN] " + s, terminal.BOLD, terminal.fg(terminal.BROWN))
        return terminal.styled_text(
            s, terminal.BOLD, terminal.fg(terminal.RED))

STREAM_HANDLER = logging.StreamHandler(stdout)
STREAM_HANDLER.setFormatter(ColoredFormater())
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.setLevel(logging.DEBUG)


ACTIONS = dict()


class MakesiteArgsParser(ArgumentParser):

    def error(self, message):
        self.print_usage(sys.stderr)
        LOGGER.info("\nInstalled templates:")
        LOGGER.debug(" ".join(get_base_templates()))
        LOGGER.info("\nInstalled modules:")
        LOGGER.debug(" ".join(get_base_modules()) + "\n")
        self.exit(2, '%s: error: %s\n' % (self.prog, message))

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        args.argv = argv
        return args


def action(*arguments, **options):
    parser = MakesiteArgsParser(
        description="'Makesite' easy control of project structure.",
        **options)
    parser.add_argument('-v', '--version', action='version',
                        version=version, help='Show makesite version')
    for (args, kwargs) in arguments:
        parser.add_argument(*args, **kwargs)

    def _inner(func):
        name = func.__name__
        parser.description = func.__doc__.strip().split('\n')[0]

        def _wrapper(params=None):
            params = parser.parse_args(params)
            return func(params)
        _wrapper.__doc__ = func.__doc__

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

    LOGGER.debug("Cmd: %s" % cmd)
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
