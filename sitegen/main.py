#!/usr/bin/env python
import ConfigParser, optparse, os, shutil, sys


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASECONFIG = os.path.join( BASEDIR, 'sitegen.ini' )
HOMECONFIG = os.path.join( os.getenv( 'HOME' ), '.sitegen.ini' )


def deploy(project_name, options):
    """ Deploy project.
    """
    __log__( "Deploy branch '%s' in project '%s'\n" % (options.branch, project_name) )
    project_options = load_config( options.config )
    deploy_dir = os.path.join( project_options[ 'Main' ][ 'sites_home' ], project_name, options.branch )

    if os.path.exists( deploy_dir ):
        __log__("Directory '%s' is exists." % deploy_dir, error=True)
        sys.exit()

    project_options[ 'Main' ].update(dict(
        project_name = project_name,
        branch = options.branch,
        deploy_dir = deploy_dir,
        repo = options.repo,
        basedir = BASEDIR,
    ))

    template_string = options.template if options.template else project_options[ 'Main' ][ 'template' ]
    templates = template_string.split(',')
    for template in templates:
        if not project_options[ 'Templates' ].has_key( template ):
            __log__( "Template '%s' not found in project_options." % template, error=True )
            sys.exit()

    templates = parse_templates(templates, project_options)
    create_dir( deploy_dir )
    open(os.path.join( deploy_dir, '.sitegen' ), 'w').write( template_string )
    deploy_templates(templates, project_options)

    os.system('chown -R %(user)s:%(group)s %(deploy_dir)s' % project_options[ 'Main' ])


def remove( project_name, options ):
    """ Remove project.
    """
    __log__( "Remove branch '%s' in project '%s'" % (options.branch, project_name))
    project_options = load_config( options.config )
    deploy_dir = os.path.join( project_options[ 'Main' ][ 'sites_home' ], project_name, options.branch )

    if not os.path.exists( deploy_dir ):
        __log__("Directory '%s' is not exists." % deploy_dir, error=True)
        sys.exit()

    project_options[ 'Main' ].update(dict(
        project_name = project_name,
        branch = options.branch,
        deploy_dir = deploy_dir,
        basedir = BASEDIR,
    ))

    try:
        sitegen_template = open(os.path.join( deploy_dir, '.sitegen', 'r' )).read()
    except IOError:
        sitegen_template = project_options[ 'Main' ][ 'template' ]

    template_string = options.template if options.template else sitegen_template
    templates = template_string.split(',')
    templates = parse_templates(templates, project_options)
    remove_templates(templates, project_options)

    __log__( "Remove directory '%s'" % deploy_dir )
    shutil.rmtree(deploy_dir)

    # If project dir empty remove it
    project_dir = os.path.dirname( deploy_dir )
    if not os.listdir(project_dir):
        __log__( "Remove directory '%s'" % project_dir )
        shutil.rmtree( project_dir )


def list_projects( options ):
    """ List projects.
    """
    project_options = load_config( options.config )
    project_dir = project_options[ 'Main' ][ 'sites_home' ]

    if not os.path.exists( project_dir ):
        __log__("Projects directory '%s' not found." % project_dir)
        sys.exit()

    for item in os.walk(project_dir):
        files = item[2]
        root = item[0]
        if '.sitegen' in files:
            branch_name = os.path.basename( root )
            project_name = os.path.basename( os.path.dirname( root ) )
            template = open( os.path.join( root, '.sitegen' ) ).read()
            __log__( "Found branch '%s' in project '%s': %s [%s]" % (branch_name, project_name, root, template))

    sys.stdout.write('\n')


def parse_templates( templates, options ):
    """ Parse templates hierarchy.
    """
    result = []
    for template in templates:
        template_options = options[ template ] if options.has_key( template ) else dict()
        if template_options.has_key( 'include' ):
            result += parse_templates( [ template_options[ 'include' ] ], options )

        result += [ ( template, template_options ) ]
    return result


def deploy_templates( templates, options ):
    """ Deploy templates.
    """
    for template_name, template_options in templates:
        path = options[ 'Templates' ][ template_name ] % options[ 'Main' ]

        # Deploy template
        __log__( "Deploy template '%s'" % template_name )
        for item in os.walk(path):
            root = item[0]
            files = item[2]
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
    """ Parse arguments and do work.
    """
    p = optparse.OptionParser(
            usage="%prog [-d] [-l] [-t TEMPLATE] [-c CONFIG] [-b BRANCH] [-r REPOSITORY] PROJECTNAME",
            description= "'sitegen' is simple script to create base project dirs and config files. ")

    p.add_option('-d', '--delete', dest='delete', help='Delete project.', action="store_true")
    p.add_option('-l', '--list', dest='list', help='List projects.', action="store_true")
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--repo', dest='repo', help='CVS repository.')

    options, args = p.parse_args()

    # List projects
    if options.list:
        list_projects(options)

    elif not args:
        p.print_help(sys.stdout)

    # Delete project
    elif options.delete:
        question = raw_input("  Delete branch '%s' on project '%s' [Y/n]?" % (options.branch, args[0]))
        if not question or question.lower().startswith('y'):
            remove( args[ 0 ], options )

    # Deploy project
    else:
        deploy(args[ 0 ], options )

