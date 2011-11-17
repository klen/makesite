import sys
from ConfigParser import ConfigParser
from os import path as op, environ, listdir, getcwd
from subprocess import CalledProcessError
from shutil import copytree

from makesite import core, settings
from makesite.engine import Engine
from makesite.utils import action, actions


@action((["PATH"], dict(help="Path to site instance.")))
def info(args):
    " Output information about site "
    path = args.PATH.rstrip(op.sep)
    output = core.get_info(path, full=True)
    core.print_header("%s -- install information" % core.get_name(path))
    print output
    return True


@action((["-p", "--path"],
    dict(help="path to makesite sites instalation dir. you can set it in $makesite_home env variable.",
        required=not bool(settings.MAKESITE_HOME),
        default=settings.MAKESITE_HOME
    )))
def ls(args):
    " Output all currently installed sites to stdout "
    core.print_header("Installed sites:")
    for site in core.get_sites(args.path):
        print core.get_info(site)
    return True


@action((["PATH"], dict(help="Project path")))
def update(args):
    " Update sites "
    path = core.get_path(args.PATH)
    for script in core.get_scripts(path, prefix='update'):
        try:
            core.call(script)
        except CalledProcessError:
            raise
    return True


@action(
    (["MODULE"], dict(help="Module name")),
    (["DEST"], dict(help="Destination", default='new_project')),
    )
def module(args):
    " Copy module source to current directory "
    mod = op.join(settings.MOD_DIR, args.MODULE)
    assert op.exists(mod), "Not found module: %s" % args.MODULE
    if not args.DEST.startswith(op.sep):
        args.DEST = op.join(getcwd(), args.DEST)
    core.print_header("Copy module source")
    copytree(mod, args.DEST)
    print "Done: %s" % args.DEST


@action((["PATH"], dict(help="Project path")))
def uninstall(args):
    " Uninstall sites "
    path = core.get_path(args.PATH)
    core.print_header('Uninstall project: %s' % path)
    for script in core.get_scripts(path, prefix='remove'):
        core.call(script)
    core.call('sudo rm -rf %s' % path)
    if not listdir(op.dirname(path)):
        core.call('sudo rm -rf %s' % op.dirname(path))


@action(
        (["ACTION"], dict(help="Choose add or remove operation", choices=("add", "remove"))),
        (["TEMPLATE"], dict(help="Name of template")),
        (["PATH"], dict(help="Project path")),)
def template(args):
    " Add or remove templates from site "
    path = args.PATH.rstrip(op.sep)
    templates = core.get_templates(path)
    parser = ConfigParser()
    tpl = op.join(settings.TPL_DIR, args.TEMPLATE)
    parser.read([
        op.join(op.dirname(path), settings.CFGNAME),
        op.join(path, settings.CFGNAME),
        op.join(tpl, settings.CFGNAME)])

    if args.ACTION == "add":
        assert not args.TEMPLATE in templates, "Template already added"
        core.print_header("Add template: %s" % args.TEMPLATE)
        templates.append(args.TEMPLATE)

        for f in core.gen_template_files(tpl):
            core.call('sudo cp %s %s' % (op.join(tpl, f), op.join(path, f)))

        for f in core.gen_template_files(tpl):
            if op.basename(op.dirname(f)) == 'service' and op.basename(f).startswith(args.TEMPLATE) and 'install' in op.basename(f):
                core.call(op.join(path, f)  )

    else:
        assert args.TEMPLATE in templates, "Template not found in project"
        core.print_header("Remove template: %s" % args.TEMPLATE)
        templates = filter(lambda x: not x == args.TEMPLATE, templates)
        tfiles = map(lambda x: op.join(path, x), core.gen_template_files(tpl))
        for f in tfiles:
            if op.basename(op.dirname(f)) == 'service' and op.basename(f).startswith(args.TEMPLATE) and 'remove' in op.basename(f):
                core.call(f)
        for f in tfiles:
            core.call('sudo rm -f %s' % f)

    core.call('sudo rm -r %s' % op.join(path, settings.TPLNAME))
    core.call('sudo sh -c "echo -n \'%s\' > %s"' % (','.join(templates), op.join(path, settings.TPLNAME)))



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
    if environ.has_key('VIRTUAL_ENV'):
        raise Exception("Please deactivate virtualenv '%s' first." % environ['VIRTUAL_ENV'])

    # Install from base modules
    if args.module:
        args.src = op.join(settings.MOD_DIR, args.module)
        assert op.exists(args.src), "Not found module: %s" % args.module

    # Fix project name
    args.PROJECT = args.PROJECT.replace('-', '_')

    args.home = op.abspath(args.path)
    args.deploy_dir = op.join(args.home, args.PROJECT, args.branch)

    # Check dir exists
    if not args.info and not args.repeat and op.exists(args.deploy_dir):
        raise Exception("\nPath %s exists. Stop deploy." % args.deploy_dir)

    # Create engine
    engine = Engine(args)

    # Show info
    if args.info:
        core.print_header('Project context', sep='-')
        print core.get_info(engine.tmp_deploy_dir, full=True)
        return True

    # Deploy src
    if not args.repeat:
        core.print_header('Deploy site', sep='-')
        core.call('sudo mkdir -p %s' % op.dirname(args.deploy_dir))
        core.call('sudo cp -r %s %s' % (engine.tmp_deploy_dir, args.deploy_dir))
        core.call('sudo chmod 0755 %s' % args.deploy_dir)

    # Run install scripts
    core.print_header('Install site', sep='-')
    core.call('sudo chmod +x %s/*.sh' % engine['service_dir'])
    for script in core.get_scripts(args.deploy_dir, prefix='install'):
        try:
            core.call(script)
        except CalledProcessError:
            print "Installation failed"
            print "Fix errors and repeat installation with (-r) or run 'makesite uninstall %s' for cancel." % args.deploy_dir
            raise


def autocomplete():
    if 'MAKESITE_AUTO_COMPLETE' not in environ:
        return
    commands = filter(lambda cmd: cmd != 'main', actions.keys())
    cwords = environ['COMP_WORDS'].split()[1:]
    cword = int(environ['COMP_CWORD'])
    try:
        current = cwords[cword-1]
    except IndexError:
        current = ''

    try:
        sub_action = [cmd for cmd in commands if cmd in cwords][0]
        if sub_action in ['info', 'uninstall', 'update', 'template']:
            if settings.MAKESITE_HOME:
                if not current or current.startswith('/'):
                    print ' '.join(site for site in core.get_sites(settings.MAKESITE_HOME) if site.startswith(current))
                else:
                    names = map(core.get_name, core.get_sites(settings.MAKESITE_HOME))
                    print ' '.join(name for name in names if name.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-m' or (current and cwords[-2] == '-m')):
            print ' '.join(mod for mod in core.get_base_modules() if mod.startswith(current))
        elif sub_action == 'install' and (cwords[-1] == '-t' or (current and cwords[-2] == '-t')):
            print ' '.join(tpl for tpl in core.get_base_templates() if tpl.startswith(current))
        elif sub_action == 'module':
            print ' '.join(tpl for tpl in core.get_base_modules() if tpl.startswith(current))
    except IndexError:
        print (' '.join(a for a in commands if a.startswith(current)))
    sys.exit(1)


@action((["action"], dict(choices=actions.keys(), help="Choose action: %s" % ', '.join(actions.keys()))))
def main(args):
    " Base dispather "
    try:
        func = actions.get(args.action)
        func(sys.argv[2:])
    except Exception, e:
        sys.stderr.write('\n' + str(e))
        print "\nSee log: %s" % core.handler.stream.name
        sys.exit(1)


def console():
    " Enter point "
    autocomplete()
    main(sys.argv[1:2])


if __name__ == '__main__':
    console()
