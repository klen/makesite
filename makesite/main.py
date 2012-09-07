import sys
from datetime import datetime
from os import path as op, environ, listdir, getcwd
from shutil import copytree
from subprocess import CalledProcessError
from socket import gaierror
from makesite import version

from . import settings
from .remote import SSHClient
from .core import ACTIONS, action, print_header, call, get_base_modules, get_base_templates, LOGFILE_HANDLER, LOGGER
from .install import Installer
from .site import Site, gen_sites, find_site


@action((["PATH"], dict(help="Path to site instance.")))
def info(args):
    " Show information about site. "

    site = find_site(args.PATH)
    print_header("%s -- install information" % site.get_name())
    LOGGER.debug(site.get_info(full=True))
    return True


@action((["-p", "--path"],
         dict(
        help="path to makesite sites instalation dir. you can set it in $makesite_home env variable.",
        required=not bool(settings.MAKESITE_HOME),
        default=settings.MAKESITE_HOME
        )))
def ls(args):
    """
    List sites
    ----------

    Show list of installed sites.

    ::

        usage: makesite ls [-h] [-v] [-p PATH]

        Show list of installed sites.

        optional arguments:
        -p PATH, --path PATH  path to makesite sites instalation dir. you can set it
                                in $makesite_home env variable.

    Examples: ::

            makesite ls

    """

    assert args.path, "Not finded MAKESITE HOME."

    print_header("Installed sites:")
    for site in gen_sites(args.path):
        LOGGER.debug(site.get_info())
    return True


@action(
    (["SITE"], dict(help="Path to site or name (project.branch)", nargs="?")),
    (["-p", "--path"],
        dict(
            help="path to makesite sites instalation dir. you can set it in $makesite_home env variable.",
            required=not bool(settings.MAKESITE_HOME),
            default=settings.MAKESITE_HOME))
)
def update(args):
    """
    Run site update
    ---------------

    Run updates for site or all installed.

    ::

        usage: main.py update [-h] [-v] [-p PATH] [SITE]

        Run site update

        positional arguments:
        SITE                  Path to site or name (project.branch)

        optional arguments:
        -p PATH, --path PATH  path to makesite sites instalation dir. you can set it
                                in $makesite_home env variable.

    Examples: ::

        # Update all makesite instances on server
        $ makesite update

        # Update by project name
        makesite update intaxi

        # Update by project name
        makesite update intaxi.develop

        # Update by project path
        makesite update /var/www/intaxi/master


    """
    if args.SITE:
        site = find_site(args.SITE, path=args.path)
        return site.run_update()

    for site in gen_sites(args.path):
        site.run_update()
    return True


@action(
    (["MODULE"], dict(help="Module name")),
    (["DEST"], dict(help="Destination", default='new_project')),
)
def module(args):
    " Copy module source to current directory. "

    mod = op.join(settings.MOD_DIR, args.MODULE)
    assert op.exists(mod), "Not found module: %s" % args.MODULE
    if not args.DEST.startswith(op.sep):
        args.DEST = op.join(getcwd(), args.DEST)
    print_header("Copy module source")
    copytree(mod, args.DEST)


@action((["PATH"], dict(help="Project path")))
def uninstall(args):
    " Uninstall site. "

    site = find_site(args.PATH)
    site.run_remove()
    site.clean()
    if not listdir(op.dirname(site.deploy_dir)):
        call('sudo rm -rf %s' % op.dirname(site.deploy_dir))


@action(
    (["ACTION"], dict(help="Choose add or remove operation",
                      choices=("add", "remove"))),
    (["TEMPLATE"], dict(help="Name of template")),
    (["PATH"], dict(help="Project path")),)
def template(args):
    " Add or remove templates from site. "
    site = Site(args.PATH)
    if args.ACTION == "add":
        return site.add_template(args.TEMPLATE)
    return site.remove_template(args.TEMPLATE)


@action(
    (["-p", "--path"], dict(
        help="path to makesite sites instalation dir. you can set it in $makesite_home env variable.",
        required=not bool(settings.MAKESITE_HOME),
        default=settings.MAKESITE_HOME
    )))
def shell(args):
    " A helper command to be used for shell integration "
    print
    print "# Makesite integration "
    print "# ==================== "
    print "export MAKESITE_HOME=%s" % args.path
    print "source %s" % op.join(settings.BASEDIR, 'shell.sh')
    print


@action(
    (["PROJECT"], dict(help="Project name")),
    (["-p", "--path"], dict(
        help="Path to makesite sites instalation dir. You can set it in $MAKESITE_HOME env variable.",
        required=not bool(settings.MAKESITE_HOME),
        default=settings.MAKESITE_HOME
    )),
    (['-b', '--branch'], dict(help='Name of branch.', default='master')),
    (['-m', '--module'], dict(help="Name of module. Install module.")),
    (['-r', '--repeat'], dict(
        action="store_true", default=False, help='Repeat installation.')),
    (['-i', '--info'], dict(action="store_true", default=False,
     help='Show project install options and exit.')),
    (['-s', '--src'], dict(help="Source path for installation.")),
    (['-t', '--template'], dict(help="Force templates.")),
    (['-c', '--config'], dict(help='Config file.', default='')),
)
def install(args):
    " Install site from sources or module "

    # Deactivate virtualenv
    if 'VIRTUAL_ENV' in environ:
        LOGGER.warning('Virtualenv enabled: %s' % environ['VIRTUAL_ENV'])

    # Install from base modules
    if args.module:
        args.src = op.join(settings.MOD_DIR, args.module)
        assert op.exists(args.src), "Not found module: %s" % args.module

    # Fix project name
    args.PROJECT = args.PROJECT.replace('-', '_')

    args.home = op.abspath(args.path)

    # Create engine
    engine = Installer(args)
    args.deploy_dir = engine.target_dir

    # Check dir exists
    assert args.info or args.repeat or not op.exists(
        engine.target_dir), "Path %s exists. Stop deploy." % args.deploy_dir

    try:
        if args.repeat:
            site = Site(engine.target_dir)
            site.run_install()
            return site

        site = engine.clone_source()
        if not site:
            return True

        engine.build()
        site.run_install()
        return site

    except (CalledProcessError, AssertionError):
        LOGGER.error("Installation failed")
        LOGGER.error("Fix errors and repeat installation with (-r) or run 'makesite uninstall %s' for cancel." % args.deploy_dir)
        raise


def autocomplete(force=False):
    " Shell autocompletion support. "

    if 'MAKESITE_AUTO_COMPLETE' not in environ and not force:
        return

    commands = filter(lambda cmd: cmd != 'main', ACTIONS.keys())

    cwords = environ['COMP_WORDS'].split()[1:]
    cword = int(environ['COMP_CWORD'])

    try:
        current = cwords[cword - 1]
    except IndexError:
        current = ''

    try:
        sub_action = [cmd for cmd in commands if cmd in cwords][0]
        if sub_action in ['info', 'uninstall', 'update', 'template']:
            if settings.MAKESITE_HOME:
                if not current or current.startswith('/'):
                    sites = list(gen_sites(settings.MAKESITE_HOME))
                    print ' '.join(site.deploy_dir for site in sites if site.
                                   deploy_dir.startswith(current))
                else:
                    names = map(lambda s: s.get_name(
                    ), gen_sites(settings.MAKESITE_HOME))
                    print ' '.join(
                        name for name in names if name.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-m' or (current and cwords[-2] == '-m')):
            print ' '.join(
                mod for mod in get_base_modules() if mod.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-t' or (current and cwords[-2] == '-t')):
            print ' '.join(tpl for tpl in get_base_templates(
            ) if tpl.startswith(current))
        elif sub_action == 'module':
            print ' '.join(
                tpl for tpl in get_base_modules() if tpl.startswith(current))
    except IndexError:
        print (' '.join(a for a in commands if a.startswith(current)))
    sys.exit(1)


@action(
    (["action"], dict(choices=ACTIONS.keys(), help="Choose action: %s" % ', '.join(ACTIONS.keys()))),
    (['-H'], dict(help="Host for run Makesite commands by ssh.", nargs="+", dest='host')),
    add_help=False
)
def main(args=None):
    " Base dispather "
    try:
        start = datetime.now()

        LOGGER.info('MAKESITE Version %s' % version)
        LOGGER.info('Started at %s' % start.strftime("%Y-%m-%d %H:%M:%S"))
        LOGGER.info('Logfile: %s' % LOGFILE_HANDLER.stream.name)
        LOGGER.info('-' * 60)

        if args.host:
            cmd = "makesite %s %s" % (args.action, ' '.join(args.argv))
            for host in args.host:
                LOGGER.info('\nHOST: %s' % host)
                LOGGER.info('RUN: %s\n' % cmd)
                client = SSHClient(host)
                client.connect()
                client.exec_command(cmd)
                client.close()
                LOGGER.info("\nOPERATION SUCCESSFUL\n")

        else:
            func = ACTIONS.get(args.action)
            func(args.argv)
            LOGGER.info("\nOPERATION SUCCESSFUL")

    except (AssertionError, CalledProcessError, gaierror), e:
        LOGGER.error("\nOPERATION FAILED - %s" % str(e))
        LOGGER.error("See log: %s" % LOGFILE_HANDLER.stream.name)
        sys.exit(1)


def console():
    " Enter point "
    autocomplete()
    config = settings.MakesiteParser()
    config.read([
        settings.BASECONFIG, settings.HOMECONFIG,
        op.join(settings.MAKESITE_HOME or '', settings.CFGNAME),
        op.join(op.curdir, settings.CFGNAME),
    ])
    argv = []
    alias = dict(config.items('alias'))
    names = alias.keys()
    for arg in sys.argv[1:]:
        if arg in names:
            argv += alias[arg].split()
            continue
        argv.append(arg)

    main(argv)


if __name__ == '__main__':
    console()
