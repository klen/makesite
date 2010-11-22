#!/usr/bin/env python
import ConfigParser, optparse, os, sys, subprocess

from sitegen import VERSION
from sitegen.template import Template


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASETEMPLATESDIR = os.path.join( BASEDIR, 'templates' )
BASECONFIG = os.path.join( BASEDIR, 'sitegen.ini' )
HOMECONFIG = os.path.join( os.getenv( 'HOME' ), '.sitegen.ini' )
SITEGENPATH_VARNAME = 'SITES_HOME'
SITEGEN_TEMPLATES_FILE = '.sitegen'
PYTHON_PREFIX = 'python' + '.'.join( str(x) for x in sys.version_info[:2] )


def deploy(project, options):
    """ Deploy project.
    """
    if os.environ.has_key( 'VIRTUAL_ENV' ):
        print "Please deactivate virtualenv '%s' first." % os.environ[ 'VIRTUAL_ENV' ]
        sys.exit()

    main_options, template_options = load_config( project, options )
    print ' \n'.join( [ "%s=%s" % item for item in main_options.items() ])
    print  "Deploy branch '%(branch)s' in project '%(project)s'\n" % main_options

    templates = parse_templates(main_options[ 'template' ].split(','), template_options)

    create_dir( main_options[ 'deploy_dir' ] )
    create_file(
        os.path.join( main_options[ 'deploy_dir' ], SITEGEN_TEMPLATES_FILE ),
        ' '.join([t[0] for t in templates]), )

    deploy_templates(templates, main_options)
    subprocess.check_call('sudo chown -R %(user)s:%(group)s %(deploy_dir)s' % main_options, shell=True)


def load_config(project, options):
    """ Load config files.
    """
    project_root = os.path.join(os.path.abspath( options.path ), 'sitegen.ini')
    paths = (BASECONFIG, HOMECONFIG, project_root, options.config or '' )
    parser = ConfigParser.RawConfigParser()
    result = dict()

    for path in paths:
        parser.read(path)
        for section in parser.sections():
            if not result.has_key( section ):
                result[ section ] = dict()
            result[ section ].update(dict(parser.items( section )))

    try:
        result[ 'Main' ].update(dict(
            project = project,
            branch = options.branch,
            python_prefix = PYTHON_PREFIX,
            deploy_dir = os.path.join( os.path.abspath( options.path ), project, options.branch ),
            basedir = BASEDIR,
            repo = options.repo if options.repo else result[ 'Main' ][ 'repo' ],
            template = options.template if options.template else result[ 'Main' ][ 'template' ]
        ))

    except KeyError:
        print "Not found currect config files."
        sys.exit()

    for opts in ( result[ 'Main' ], result[ 'Templates' ] ):
        for key, value in opts.items():
            opts[ key ] = Template.sub( value, **result[ 'Main' ] )

    return result[ 'Main' ], result[ 'Templates' ]


def parse_templates( templates, options ):
    """ Parse templates hierarchy.
    """
    result = []

    for template in templates:
        path = options[ template ] if options.has_key( template ) else os.path.join( BASETEMPLATESDIR, template )
        if not os.path.exists( path ):
            print  "Template '%s' not found in base and custom templates." % template
            sys.exit()

        try:
            f = open( os.path.join( path, SITEGEN_TEMPLATES_FILE ), 'r' )
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
            curdir = os.path.join( main_options[ 'deploy_dir' ], root[ len( path ) + 1: ] )
            main_options[ 'curdir' ] = curdir
            create_dir( curdir )
            for filename in files:
                if filename == SITEGEN_TEMPLATES_FILE:
                    continue
                t = Template(filename=os.path.join( root, filename ))
                create_file(os.path.join( curdir, filename ), t(**main_options))

        sys.stdout.write('\n')

    subprocess.check_call('sitegenparse %(deploy_dir)s install' % main_options, shell=True)


def create_dir(path):
    """ Create directory.
    """
    try:
        subprocess.check_call('sudo mkdir -p %s' % path, shell=True)
        print "Create dir %s." % path
    except subprocess.CalledProcessError:
        print "Sitegen need sudo access."
        sys.exit()


def create_file( path, s ):
    """ Create file.
    """
    try:
        open('/tmp/sitegen.tmp', 'w').write(s)
        subprocess.check_call('sudo mv /tmp/sitegen.tmp %s' % path, shell=True)
        print "Create file '%s'" % path
    except subprocess.CalledProcessError:
        print 'Failed create file %s.' % path


def main():
    """ Parse arguments and do work.
    """
    path = os.environ[ SITEGENPATH_VARNAME ] if os.environ.has_key( SITEGENPATH_VARNAME ) else None
    p = optparse.OptionParser(
            usage="%prog -p PATH PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-r REPOSITORY]",
            version='%prog ' + VERSION,
            description= "'sitegen' is simple script to create base project dirs and config files. ")
    p.add_option('-p', '--path', dest='path', default=path, help='Path to project dir. Required option.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--repo', dest='repo', help='CVS repository.')

    options, args = p.parse_args()

    if not options.path or not args:
        p.print_help(sys.stdout)

    else:
        deploy( args[0], options )

