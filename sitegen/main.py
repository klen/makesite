#!/usr/bin/env python
import ConfigParser, optparse, os, shutil, sys, tempita


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASECONFIG = os.path.join( BASEDIR, 'sitegen.ini' )
HOMECONFIG = os.path.join( os.getenv( 'HOME' ), '.sitegen.ini' )


def do_work(project_name, options):
    """ Parse options and do work.
    """
    project_options = load_config( options )
    project_options[ 'Main' ].update(dict(
        project_name = project_name,
        branch = options.branch,
        deploy_dir = os.path.join( os.path.abspath( options.path ), project_name, options.branch ),
        basedir = BASEDIR,
    ))
    project_options[ 'Main' ][ 'repo' ] = options.repo if options.repo else project_options[ 'Main' ][ 'repo' ]
    project_options[ 'Main' ][ 'template' ] = options.template if options.template else project_options[ 'Main' ][ 'template' ]
    for key, value in project_options[ 'Main' ].items():
        project_options[ 'Main' ][ key ] = value % project_options[ 'Main' ]

    __log__("Options:")
    for item in project_options[ 'Main' ].items():
        __log__("%s: %s" % item )

    if options.delete:
        remove( project_options )

    else:
        deploy( project_options )


def deploy(options):
    """ Deploy project.
    """
    main_options = options[ 'Main' ]
    __log__( "Deploy branch '%(branch)s' in project '%(project_name)s'\n" % main_options )

    if os.path.exists( main_options[ 'deploy_dir' ] ):
        __log__("Directory '%(deploy_dir)s' is exists." % main_options, error=True)
        sys.exit()

    template_string = main_options[ 'template' ]
    templates = template_string.split(',')
    for template in templates:
        if not options[ 'Templates' ].has_key( template ):
            __log__( "Template '%s' not found in project_options." % template, error=True )
            sys.exit()

    templates = parse_templates(templates, options)
    create_dir( main_options[ 'deploy_dir' ] )
    open(os.path.join( main_options[ 'deploy_dir' ], '.sitegen' ), 'w').write( template_string )
    deploy_templates(templates, options)

    os.system('chown -R %(user)s:%(group)s %(deploy_dir)s' % main_options)


def remove( options ):
    """ Remove project.
    """
    main_options = options[ 'Main' ]
    question = raw_input("\n  Delete branch '%(branch)s' on project '%(project_name)s' [Y/n]?" % main_options)
    if question and not question.lower().startswith('y'):
        sys.exit()

    __log__("Remove branch '%(branch)s' in project '%(project_name)s'" % main_options)

    if not os.path.exists( main_options[ 'deploy_dir' ] ):
        __log__("Directory '%s' is not exists." % main_options[ 'deploy_dir' ], error=True)
        sys.exit()

    try:
        template_string = open(os.path.join( main_options[ 'deploy_dir' ], '.sitegen', 'r' )).read()
    except IOError:
        template_string = options[ 'Main' ][ 'template' ]

    templates = template_string.split(',')
    templates = parse_templates(templates, options)
    remove_templates(templates, options)

    __log__( "Remove directory '%s'" % main_options[ 'deploy_dir' ])
    shutil.rmtree(main_options[ 'deploy_dir' ])

    # If project dir empty remove it
    project_dir = os.path.dirname( main_options[ 'deploy_dir' ] )
    if not os.listdir(project_dir):
        __log__( "Remove directory '%s'" % project_dir )
        shutil.rmtree( project_dir )


def list_projects( options ):
    """ List projects.
    """
    project_dir = os.path.abspath( options.path )

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


def load_config(options):
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

    if not result or not result.has_key( 'Main' ) or not result.has_key( 'Templates' ):
        __log__("Not found currect config files.", error=True)
        sys.exit()

    return result


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
                f = open(os.path.join(root, filename))
                s = tempita.sub( f.read(), **options[ 'Main' ] )
                create_file(os.path.join(curdir, filename), s)

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
            usage="%prog -p PATH [-l] PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-r REPOSITORY] [-d]",
            description= "'sitegen' is simple script to create base project dirs and config files. ")
    p.add_option('-p', '--path', dest='path', help='Path to project dir. Required option.')
    p.add_option('-l', '--list', dest='list', help='List projects.', action="store_true")
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--repo', dest='repo', help='CVS repository.')
    p.add_option('-d', '--delete', dest='delete', help='Delete project.', action="store_true")

    options, args = p.parse_args()

    if not options.path:
        p.print_help(sys.stdout)

    elif options.list:
        list_projects(options)

    elif not args:
        p.print_help(sys.stdout)

    else:
        do_work( args[0], options )

