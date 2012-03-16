import sys
from os import path as op, environ, listdir, getcwd
from shutil import copytree
from subprocess import CalledProcessError

from makesite import settings
from makesite.core import ACTIONS, action, print_header, call, get_base_modules, get_base_templates, LOGFILE_HANDLER
from makesite.install import Installer
from makesite.site import Site, gen_sites, find_site


@action((["PATH"], dict(help="Path to site instance.")))
def info(args):
    " Show information about installed site. "
    site = find_site(args.PATH)
    print_header("%s -- install information" % site.get_name())
    print site.get_info(full=True)
    return True


@action((["-p", "--path"],
    dict(help="path to makesite sites instalation dir. you can set it in $makesite_home env variable.",
        required=not bool(settings.MAKESITE_HOME),
        default=settings.MAKESITE_HOME
    )))
def ls(args):
    " Show list of currently installed sites. "
    print_header("Installed sites:")
    for site in gen_sites(args.path):
        print site.get_info()
    return True


@action((["PATH"], dict(help="Project path")))
def update(args):
    " Update sites "
    path = args.PATH
    site = find_site(path)
    return site.run_update()


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
    print "Done: %s" % args.DEST


@action((["PATH"], dict(help="Project path")))
def uninstall(args):
    " Uninstall sites "
    site = find_site(args.PATH)
    site.run_remove()
    site.clean()
    if not listdir(op.dirname(site.deploy_dir)):
        call('sudo rm -rf %s' % op.dirname(site.deploy_dir))


@action(
        (["ACTION"], dict(help="Choose add or remove operation", choices=("add", "remove"))),
        (["TEMPLATE"], dict(help="Name of template")),
        (["PATH"], dict(help="Project path")),)
def template(args):
    " Add or remove templates from site "
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
    (['-r', '--repeat'], dict(action="store_true", default=False, help='Repeat installation.')),
    (['-i', '--info'], dict(action="store_true", default=False, help='Show project install options and exit.')),
    (['-s', '--src'], dict(help="Source path for installation.")),
    (['-t', '--template'], dict(help="Force templates.")),
    (['-c', '--config'], dict(help='Config file.', default='')),
)
def install(args):
    " Install site from sources or module "

    # Deactivate virtualenv
    _check_virtualenv()

    # Install from base modules
    if args.module:
        args.src = op.join(settings.MOD_DIR, args.module)
        assert op.exists(args.src), "Not found module: %s" % args.module

    # Fix project name
    args.PROJECT = args.PROJECT.replace('-', '_')

    args.home = op.abspath(args.path)
    args.deploy_dir = op.join(args.home, args.PROJECT, args.branch)

    # Create engine
    engine = Installer(args)

    # Check dir exists
    if not args.info and not args.repeat and op.exists(args.deploy_dir):
        raise Exception("\nPath %s exists. Stop deploy." % args.deploy_dir)

    try:
        if args.repeat:
            site = Site(args.deploy_dir)
            site.run_install()
            return site

        site = engine.clone_source()
        if not site:
            return True

        engine.build()
        site.run_install()
        return site

    except (CalledProcessError, AssertionError):
        print "Installation failed"
        print "Fix errors and repeat installation with (-r) or run 'makesite uninstall %s' for cancel." % args.deploy_dir
        raise


def autocomplete():
    if 'MAKESITE_AUTO_COMPLETE' not in environ:
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
                    print ' '.join(site.deploy_dir for site in sites if site.deploy_dir.startswith(current))
                else:
                    names = map(lambda s: s.get_name(), gen_sites(settings.MAKESITE_HOME))
                    print ' '.join(name for name in names if name.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-m' or (current and cwords[-2] == '-m')):
            print ' '.join(mod for mod in get_base_modules() if mod.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-t' or (current and cwords[-2] == '-t')):
            print ' '.join(tpl for tpl in get_base_templates() if tpl.startswith(current))
        elif sub_action == 'module':
            print ' '.join(tpl for tpl in get_base_modules() if tpl.startswith(current))
    except IndexError:
        print (' '.join(a for a in commands if a.startswith(current)))
    sys.exit(1)


@action((["action"], dict(choices=ACTIONS.keys(), help="Choose action: %s" % ', '.join(ACTIONS.keys()))))
def main(args):
    " Base dispather "
    try:
        func = ACTIONS.get(args.action)
        func(sys.argv[2:])
    except AssertionError, e:
        sys.stderr.write('\n' + str(e))
        print "\nSee log: %s" % LOGFILE_HANDLER.stream.name
        sys.exit(1)


def console():
    " Enter point "
    autocomplete()
    main(sys.argv[1:2])


def _check_virtualenv():
    if 'VIRTUAL_ENV' in environ:
        raise Exception("Please deactivate virtualenv '%s' first." % environ['VIRTUAL_ENV'])


if __name__ == '__main__':
    console()
