#!/usr/bin/env python
import ConfigParser, optparse, os, sys, subprocess

from makesite import VERSION, INI_FILENAME, TEMPLATES_FILE
from makesite.template import Template


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASE_TEMPLATES_DIR = os.path.join(BASEDIR, 'templates')
MODULES_DIR = os.path.join(BASEDIR, 'modules')

PATH_VARNAME = 'SITES_HOME'

BASECONFIG = os.path.join( BASEDIR, INI_FILENAME )
HOMECONFIG = os.path.join( os.getenv('HOME'), INI_FILENAME )

PYTHON_PREFIX = 'python' + '.'.join( str(x) for x in sys.version_info[:2] )


def deploy(project, options):
    """ Deploy project.
    """
    # This not work in virtual env
    if os.environ.has_key('VIRTUAL_ENV'):
        print "Please deactivate virtualenv '%s' first." % os.environ['VIRTUAL_ENV']
        sys.exit()

    # Compile project options
    main_options, template_options = load_config(project, options)

    # Get templates
    templates = parse_templates(main_options['template'].split(','), template_options)
    main_options['template'] = ' '.join([t[0] for t in templates ])

    # Show project options
    print  "\nDeploy branch '%(branch)s' in project '%(project)s'\n" % main_options
    print get_options(main_options)
    print

    # Exit if requested only info
    if options.info:
        sys.exit()

    # Check path exists
    if os.path.exists(main_options['deploy_dir']):
        print "\n %s exists. Stop deploy." % main_options['deploy_dir']
        sys.exit()

    # Create dir and makesite templates file
    create_dir( main_options[ 'deploy_dir' ] )
    create_file(os.path.join( main_options[ 'deploy_dir' ], TEMPLATES_FILE ), ' '.join([t[0] for t in templates]))
    create_file(os.path.join(main_options['deploy_dir'], INI_FILENAME), "[Main]\n%s" % get_options(main_options))

    # Deploy templates
    deploy_templates(templates, main_options)

    # Run install site
    subprocess.check_call('makesiteparse %(deploy_dir)s install' % main_options, shell=True)


def get_options(main_options):
    keys = main_options.keys()
    keys.sort()
    return ' \n'.join(["{0:<20} = {1}".format(key, main_options[key]) for key in keys])


def load_config(project, options):
    """ Load config files.
    """

    if options.module:
        config = os.path.join(options.module, INI_FILENAME)
        if not os.path.exists(config):
            config = os.path.join(MODULES_DIR, options.module, INI_FILENAME)
    else:
        config = options.config or ''


    # Deploy projects dir
    projects_dir = os.path.join(os.path.abspath(options.path), INI_FILENAME)

    # Load config in this order
    paths = (BASECONFIG, HOMECONFIG, projects_dir, config)
    parser = ConfigParser.RawConfigParser()
    result = dict()

    for path in paths:
        parser.read(path)
        for section in parser.sections():
            if not result.has_key( section ):
                result[ section ] = dict()
            result[ section ].update(dict(parser.items( section )))

    # Default params
    try:
        result['Main'].update(dict(
            project = project,
            branch = options.branch,
            sitesdir = options.path,
            python_prefix = PYTHON_PREFIX,
            deploy_dir = os.path.join( os.path.abspath( options.path ), project, options.branch ),
            basedir = BASEDIR,
            repo = options.repo if options.repo else result[ 'Main' ][ 'repo' ],
            template = options.template if options.template else result[ 'Main' ][ 'template' ]
        ))

    except KeyError:
        print "Not found currect config files."
        sys.exit()

    # Path for install from dir (config file in this dir)
    if config:
        result['Main']['sourcedir'] = os.path.abspath(os.path.dirname(config))

    # Parse options template
    for opts in ( result['Main'], result['Templates'] ):
        for key, value in opts.items():
            opts[key] = Template.sub( value, **result['Main'] )

    return result['Main'], result['Templates']


def parse_templates( templates, options ):
    """ Parse templates hierarchy.
    """
    result = list()

    for template in templates:
        path = options[template] if options.has_key(template) else os.path.join( BASE_TEMPLATES_DIR, template )
        if not os.path.exists( path ):
            print  "Template '%s' not found in base and custom templates." % template
            sys.exit()

        try:
            f = open( os.path.join( path, TEMPLATES_FILE ), 'r' )
            child = f.read().strip()
            result += parse_templates( child.split(' '), options )
        except IOError:
            pass

        result.append(( template, path ))

    return result


def deploy_templates( templates, main_options ):
    """ Deploy templates.
    """
    for template, path in templates:
        print "Deploy template '%s'." % template
        for item in os.walk(path):
            root = item[0]
            files = item[2]
            curdir = os.path.join(main_options['deploy_dir'], root[len( path ) + 1:])
            main_options[ 'curdir' ] = curdir
            create_dir( curdir )
            for filename in files:
                if filename == TEMPLATES_FILE:
                    continue
                t = Template(filename=os.path.join( root, filename ))
                create_file(os.path.join( curdir, filename ), t(**main_options))

        sys.stdout.write('\n')


def create_dir(path):
    """ Create directory.
    """
    try:
        subprocess.check_call('sudo mkdir -p %s' % path, shell=True)
        print "Create dir %s." % path
    except subprocess.CalledProcessError:
        print "makesite need sudo access."
        sys.exit()


def create_file( path, s ):
    """ Create file.
    """
    try:
        open('/tmp/makesite.tmp', 'w').write(s)
        subprocess.check_call('sudo mv /tmp/makesite.tmp %s' % path, shell=True)
        print "Create file '%s'" % path
    except subprocess.CalledProcessError:
        print 'Failed create file %s.' % path


def main():
    """ Parse arguments and do work.
    """
    path = os.environ[ PATH_VARNAME ] if os.environ.has_key( PATH_VARNAME ) else None
    p = optparse.OptionParser(
            usage="%prog -p PATH PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-r REPOSITORY] [-m MODULENAME or MODULEPATH]",
            version='%prog ' + VERSION,
            description= "'Makesite' is scripts collection for create base project dirs and config files. \n See also next utilities: installsite, updatesite, removesite, cdsite, worksite, lssites, statsites.")
    p.add_option('-p', '--path', dest='path', default=path, help='Path to project dir. Required option.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--repo', dest='repo', help='VCS repository address.')
    p.add_option('-m', '--module', dest="module", help="Deploy module")
    p.add_option('-i', '--info', dest='info', action="store_true", default=False, help='Show compiled project params without action.')

    options, args = p.parse_args()

    if not options.path or not args:
        p.print_help(sys.stdout)

    else:
        deploy( args[0], options )

