#!/usr/bin/env python

import ConfigParser, optparse, os, shutil, sys

BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASECONFIG = os.path.join( BASEDIR, 'sitegen.ini' )
HOMECONFIG = os.path.join( os.getenv( 'HOME' ), '.sitegen.ini' )


def deploy(project_name, template=None, config=None, branch=None):
    """ Deploy project.
    """
    __log__( "Deploy branch '%s' in project '%s'\n" % (branch, project_name) )
    options = load_config( config )
    deploy_dir = os.path.join( options[ 'Main' ][ 'sites_home' ], project_name, branch )

    if os.path.exists( deploy_dir ):
        __log__("Directory '%s' is exists." % deploy_dir, error=True)
        sys.exit()

    options[ 'Main' ].update(dict(
        project_name = project_name,
        branch = branch,
        deploy_dir = deploy_dir,
        basedir = BASEDIR,
    ))

    template = template if template else options[ 'Main' ][ 'template' ]
    if not options[ 'Templates' ].has_key( template ):
        __log__( "Template '%s' not found in options." % template, error=True )
        sys.exit()

    templates = parse_templates(template, options)
    deploy_templates(templates, options)
    os.system('chown -R %(user)s:%(group)s %(deploy_dir)s' % options[ 'Main' ])


def remove( project_name, template=None, config=None, branch=None ):
    """ Remove project.
    """
    __log__( "Remove branch '%s' in project '%s'" % (branch, project_name))
    options = load_config( config )
    deploy_dir = os.path.join( options[ 'Main' ][ 'sites_home' ], project_name, branch )

    if not os.path.exists( deploy_dir ):
        __log__("Directory '%s' is not exists." % deploy_dir, error=True)
        sys.exit()

    options[ 'Main' ].update(dict(
        project_name = project_name,
        branch = branch,
        deploy_dir = deploy_dir,
        basedir = BASEDIR,
    ))

    template = template if template else options[ 'Main' ][ 'template' ]
    templates = parse_templates(template, options)
    remove_templates(templates, options)
    __log__( "Remove directory '%s'" % deploy_dir )
    shutil.rmtree(deploy_dir)


def parse_templates( template, options ):
    """ Parse templates hierarchy.
    """
    result = []
    template_options = options[ template ] if options.has_key( template ) else dict()
    if template_options.has_key( 'include' ):
        result += parse_templates( template_options[ 'include' ], options )

    result += [ ( template, template_options ) ]
    return result


def deploy_templates( templates, options ):
    """ Deploy templates.
    """
    for template_name, template_options in templates:
        path = options[ 'Templates' ][ template_name ] % options[ 'Main' ]

        # Deploy template
        __log__( "Deploy template '%s'" % template_name )
        for root, dirs, files in os.walk(path):
            curdir = os.path.join( options[ 'Main' ][ 'deploy_dir' ], root[ len( path ) + 1: ] )
            options[ 'Main' ][ 'curdir' ] = curdir
            create_dir( curdir )
            for filename in files:
                name, ext = os.path.splitext(filename)
                f = open(os.path.join(root, filename))
                if ext == '.tpl':
                    s = f.read() % options[ 'Main' ]
                else:
                    name = name + ext
                    s = f.read()

                create_file(os.path.join(curdir, name), s)

        # Parse hook
        if template_options.has_key( 'install_hook' ):
            hook = template_options[ 'install_hook' ]
            path = os.path.join( options[ 'Main' ][ 'deploy_dir' ], hook )
            __log__( "Start hook script '%s'" % path )
            os.system( 'sh %s' % path )

        sys.stdout.write('\n')


def remove_templates( templates, options ):
    """ Remove templates.
    """
    for template_name, template_options in templates:
        # Remove template
        __log__( "Remove template '%s'" % template_name )
        if template_options.has_key( 'remove_hook' ):
            hook = template_options[ 'remove_hook' ]
            path = os.path.join( options[ 'Main' ][ 'deploy_dir' ], hook )
            __log__( "Start hook script '%s'" % path )
            os.system( 'sh %s' % path )

        sys.stdout.write('\n')


def load_config(config):
    """ Load config files.
    """
    paths = (BASECONFIG, HOMECONFIG, config or '' )
    parser = ConfigParser.RawConfigParser()
    result = dict()

    for path in paths:
        parser.read(path)
        for section in parser.sections():
            if not result.has_key( section ):
                result[ section ] = dict()
            result[ section ].update(dict(parser.items( section )))

    if not result or not result.has_key( 'Main' ) or not result.has_key( 'Templates' ):
        __log__("Not found currect config files.", error=True)
        sys.exit()

    return result


def create_dir(path):
    """ Create directory.
    """
    if os.path.exists( path ):
        return
    try:
        os.makedirs(path)
        __log__( "Create dir '%s'" % path )
    except(OSError), e:
        __log__( "Failed create dir '%s'. %s." % (path, e.strerror), error=True )
        sys.exit()


def create_file( path, s ):
    """ Create file.
    """
    try:
        f = open(path, 'w')
        f.write(s)
        __log__( "Create file '%s'" % path )
    except (IOError, OSError), e:
        __log__('Failed create file "%s". %s.\n'
            % (path, e.strerror), error=True)


def __log__( s, error=False ):
    """ Print messages.
    """
    s = "\n  * %s" % s
    if error:
        sys.stderr.write(s)
    else:
        sys.stdout.write(s)

def main():
    p = optparse.OptionParser(
            usage="%prog [-r] [-t TEMPLATE] [-c CONFIGFILE] [-b BRANCHNAME] PROJECTNAME",
            description= "'sitegen' is simple script to create base project dirs and config files. ")

    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--remove', dest='remove', help='Remove project.', action="store_true")

    options, args = p.parse_args()
    if not args:
        p.print_help(sys.stdout)
        sys.exit()

    if options.remove:
        # Remove project
        remove( args[ 0 ], template=options.template, config=options.config, branch=options.branch )

    else:
        # Deploy project
        deploy(args[ 0 ], template=options.template, config=options.config, branch=options.branch)

