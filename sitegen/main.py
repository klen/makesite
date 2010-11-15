#!/usr/bin/env python
import ConfigParser, optparse, os, sys, tempita, subprocess


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASECONFIG = os.path.join( BASEDIR, 'sitegen.ini' )
HOMECONFIG = os.path.join( os.getenv( 'HOME' ), '.sitegen.ini' )
SITEGEN_PATH_VAR = 'SITES_HOME'


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

    for item in project_options[ 'Main' ].items():
        print " %s=%s" % item

    if options.delete:
        remove( project_options )

    else:
        deploy( project_options )


def deploy(options):
    """ Deploy project.
    """
    main_options = options[ 'Main' ]
    print  "Deploy branch '%(branch)s' in project '%(project_name)s'\n" % main_options

    template_string = main_options[ 'template' ]
    templates = template_string.split(',')
    for template in templates:
        if not options[ 'Templates' ].has_key( template ):
            print  "Template '%s' not found in project_options." % template
            sys.exit()

    templates = parse_templates(templates, options)
    create_dir( main_options[ 'deploy_dir' ] )
    subprocess.call('sudo sh -c "echo -n %s > %s/.sitegen"' % ( template_string, main_options[ 'deploy_dir' ]), shell=True)
    deploy_templates(templates, options)

    subprocess.check_call('sudo chown -R %(user)s:%(group)s %(deploy_dir)s' % main_options, shell=True)


def remove( options ):
    """ Remove project.
    """
    main_options = options[ 'Main' ]
    question = raw_input("\n  Delete branch '%(branch)s' on project '%(project_name)s' [Y/n]?" % main_options)
    if question and not question.lower().startswith('y'):
        sys.exit()

    print "Remove branch '%(branch)s' in project '%(project_name)s'" % main_options

    if not os.path.exists( main_options[ 'deploy_dir' ] ):
        print "Directory '%s' is not exists." % main_options[ 'deploy_dir' ]
        sys.exit()

    try:
        template_string = open(os.path.join( main_options[ 'deploy_dir' ], '.sitegen', 'r' )).read()
    except IOError:
        template_string = options[ 'Main' ][ 'template' ]

    templates = template_string.split(',')
    templates = parse_templates(templates, options)
    remove_templates(templates, options)

    print "Remove directory '%s'" % main_options[ 'deploy_dir' ]
    subprocess.check_call(" sudo rm -rf %s" % main_options[ 'deploy_dir' ], shell=True)

    # If project dir empty remove it
    project_dir = os.path.dirname( main_options[ 'deploy_dir' ] )
    if not os.listdir(project_dir):
        print "Remove directory '%s'" % project_dir
        subprocess.check_call(" sudo rm -rf %s" % project_dir, shell=True)


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
        print "Not found currect config files."
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
        print "Deploy template '%s'" % template_name
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
            print "Start hook script '%s'" % path
            subprocess.call('sudo sh %s' % path, shell=True)

        sys.stdout.write('\n')


def remove_templates( templates, options ):
    """ Remove templates.
    """
    for template_name, template_options in templates:
        # Remove template
        print "Remove template '%s'" % template_name
        if template_options.has_key( 'remove_hook' ):
            hook = template_options[ 'remove_hook' ]
            path = os.path.join( options[ 'Main' ][ 'deploy_dir' ], hook )
            print "Start hook script '%s'" % path
            subprocess.call('sudo sh %s' % path, shell=True)

        sys.stdout.write('\n')



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
    path = os.environ[ SITEGEN_PATH_VAR ] if os.environ.has_key( SITEGEN_PATH_VAR ) else None
    p = optparse.OptionParser(
            usage="%prog -p PATH [-l] PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-r REPOSITORY] [-d]",
            description= "'sitegen' is simple script to create base project dirs and config files. ")
    p.add_option('-p', '--path', dest='path', default=path, help='Path to project dir. Required option.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-r', '--repo', dest='repo', help='CVS repository.')
    p.add_option('-d', '--delete', dest='delete', help='Delete project.', action="store_true")

    options, args = p.parse_args()

    if not options.path or not args:
        p.print_help(sys.stdout)

    else:
        do_work( args[0], options )

