import logging
from os import walk, path as op, listdir, access, X_OK, environ, makedirs, pathsep
from shutil import copy2
from subprocess import check_call
from tempfile import mktemp, mkdtemp

from makesite.settings import CFGNAME, TPLNAME, TPL_DIR, MOD_DIR
from makesite.template import Template


logger = logging.getLogger('Makesite')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(mktemp())
logger.addHandler(handler)


def walklevel(dirpath, level=1):
    dirpath = dirpath.rstrip(op.sep)
    assert op.isdir(dirpath)
    start = dirpath.count(op.sep)
    for root, dirs, files in walk(dirpath):
        yield root, dirs, files
        if start + level <= root.count(op.sep):
            del dirs[:]


def is_project(path):
    path = op.join(path, TPLNAME)
    return op.exists(path) and op.isfile(path)


def check_project(path):
    if not is_project(path):
        raise Exception("Invalid makesite-project: %s" % path)


def print_header(msg, sep='='):
    logger.debug("\n%s\n%s" % (msg, ''.join(sep for _ in msg)))
    print "\n%s\n%s" % (msg, ''.join(sep for _ in msg))


def get_templates(path):
    try:
        return open(op.join(path, TPLNAME)).read().strip().split(',')
    except IOError:
        raise Exception("Invalid makesite-project: %s" % path)


def get_base_modules():
    return sorted(filter(
            lambda x: op.isdir(op.join(MOD_DIR, x)),
            listdir(MOD_DIR)))


def get_base_templates():
    return sorted(filter(
            lambda x: op.isdir(op.join(TPL_DIR, x)),
            listdir(TPL_DIR)))


def get_sites(path):
    for root, _, _ in walklevel(path, 2):
        if is_project(root):
            yield root


def get_name(path):
    return "%s.%s" % (op.basename(path), op.basename(op.dirname(path)))


def get_info(path, full=False):
    try:
        if full:
            return open(op.join(path, CFGNAME)).read()
        return "%s [%s]" % (get_name(path), open(op.join(path, TPLNAME)).read())
    except IOError:
        raise Exception("Invalid makesite-project: %s" % path)


def get_scripts(path, prefix=None):
    check_project(path)
    service_dir = op.join(path, "service")
    templates = get_templates(path)
    files = listdir(service_dir)
    result = []
    for template in templates:
        result += filter(is_exe,
            map(lambda x: op.join(service_dir, x),
                    filter(lambda x: x.startswith(template) and (not prefix or prefix in x), files)))
    return result


def is_exe(path):
    return op.exists(path) and access(path, X_OK)


def which(program):
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
    logger.debug("Cmd: %s" % cmd)
    print "Cmd: %s" % cmd
    check_call(cmd, shell=shell, stdout=handler.stream, **kwargs)


def gen_template_files(path):
    " Generate relative template pathes "
    path = path.rstrip(op.sep)
    for root, _, files in walk(path):
        for f in filter(lambda x: not x in (TPLNAME, CFGNAME), files):
            yield op.relpath(op.join(root, f), path)


def prepare_template(name, path, parser, destination=None):
    print "Prepare template: %s" % name

    destination = destination or mkdtemp()
    parser.read(op.join(path, CFGNAME), extending=True)
    context = dict(parser.items('Main'))

    for f in gen_template_files(path):
        curdir = op.join(destination, op.dirname(f))
        if not op.exists(curdir):
            makedirs(curdir)

        source = op.join(path, f)
        target = op.join(destination, f)
        copy2(source, target)
        if not (f.startswith('bin') or f.startswith('static')):
            Template(filename=target, context=context).parse_file()

    return destination
