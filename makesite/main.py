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
        print >> sys.stderr, "Please deactivate virtualenv '%s' first." % os.environ['VIRTUAL_ENV']
        sys.exit(1)

    # Compile project options
    options = load_config(project, options)

    # Exit if requested only info
    if options['Main']['info']:
        print format_options(options['Main'])
        sys.exit()

    # Check path exists
    if os.path.exists(options['Main']['deploy_dir']):
        print >> sys.stderr, "\nPath %s exists. Stop deploy." % options['Main']['deploy_dir']
        sys.exit(1)

    # Create dir and makesite templates file
    create_dir( options['Main'][ 'deploy_dir' ] )

    # Load source
    base_templates = load_source(options)

    # Get templates
    templates = base_templates + options['Main']['template'].split(',')
    templates = parse_templates(templates, options['Templates'])
    options['Main']['template'] = ' '.join([t[0] for t in templates ])

    # Show project options
    print  "\nDeploy branch '%(branch)s' in project '%(project)s'\n" % options['Main']
    print format_options(options['Main'])
    print

    # Create makesite project files
    create_file(os.path.join( options['Main'][ 'deploy_dir' ], TEMPLATES_FILE ), ' '.join([t[0] for t in templates]))
    create_file(os.path.join(options['Main']['deploy_dir'], INI_FILENAME), "[Main]\n%s" % format_options(options['Main']))

    # Deploy templates
    for template, path in templates:
        if template != 'base':
            deploy_template(path, options['Main'], template)

    # Run install site
    subprocess.check_call('makesiteparse %(deploy_dir)s install' % options['Main'], shell=True)


def format_options(main_options):
    """ Return string with sorted and formated options list.
    """
    keys = main_options.keys()
    keys.sort()
    return ' \n'.join(["{0:<20} = {1}".format(key, main_options[key]) for key in keys])


def load_config(project, options):
    """ Load config files.
    """
    # Deploy projects dir
    projects_dir = os.path.join(os.path.abspath(options.path), INI_FILENAME)

    # Load config in this order
    result = dict(Main = dict(
        basedir = BASEDIR,
        project = project,
        python_prefix = PYTHON_PREFIX,
        branch = options.branch,
        sites_home = options.path,
        deploy_dir = os.path.join( os.path.abspath( options.path ), project, options.branch ),
        info = options.info,
    ))

    # Load base configs
    for path in (BASECONFIG, HOMECONFIG, projects_dir, options.config or ''):
        parse_config(path, result)

    src = options.src or result['Main'].get('src', None)
    if options.module:
        src = os.path.join(MODULES_DIR, options.module)
        if not os.path.exists(src):
            print >> sys.stderr, "Not found module: %s" % options.module
            sys.exit()

    if options.template:
        result['Main']['template'] = options.template

    result['Main']['src'] = os.path.abspath(src) if src and not '+' in src else src
    return result


def load_source(options):
    """ Deploy base template and load source.
    """

    if options['Main']['src']:
        template = 'src-dir'
        if options['Main']['src'].startswith('git+'):
            options['Main']['src'] = options['Main']['src'][4:]
            template = 'src-git'

        deploy_template(options['Templates']['base'], options['Main'], 'base')
        try:
            subprocess.check_call('sh %s/%s_init.sh' % (options['Main']['project_servicedir'], template), shell=True)
        except subprocess.CalledProcessError:
            subprocess.check_call('sudo rm -rf %s' % options['Main']['deploy_dir'], shell=True)
            print >> sys.stderr, "Error deploy src: %s" % options['Main']['src']
            sys.exit(1)

        parse_config(os.path.join( options['Main']['project_sourcedir'], INI_FILENAME ), options)
        return [ 'base', template ]

    deploy_template(options['Templates']['base'], options['Main'], 'base')
    return [ 'base' ]


def parse_config(path, result):
    """ Parse config file.
    """
    parser = ConfigParser.RawConfigParser()
    parser.read(path)
    for section in parser.sections():
        if not result.has_key( section ):
            result[ section ] = dict()
        data = dict(parser.items( section ))
        # Parse options template
        for k, v in data.items():
            data[k] = Template.sub(v, **result['Main'])
        result[ section ].update(data)


def parse_templates( templates, options ):
    """ Parse templates hierarchy.
    """
    result = list()

    for template in templates:
        path = options[template] if options.has_key(template) else os.path.join( BASE_TEMPLATES_DIR, template )
        if not os.path.exists( path ):
            print >> sys.stderr, "Template '%s' not found in base and custom templates." % template
            sys.exit(1)

        try:
            f = open( os.path.join( path, TEMPLATES_FILE ), 'r' )
            child = f.read().strip()
            result += parse_templates( child.split(' '), options )
        except IOError:
            pass

        result.append(( template, path ))

    return result


def deploy_template(path, main_options, template):
    """ Deploy template.
    """
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
        print >> sys.stderr, "makesite need sudo access."
        sys.exit(1)


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
            usage="%prog -p PATH PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-s SOURCE_PATH] [-m MODULENAME or MODULEPATH] [-i]",
            version='%prog ' + VERSION,
            description= "'Makesite' is scripts collection for create base project dirs and config files. \n See also next utilities: installsite, updatesite, removesite, cdsite, worksite, lssites, statsites.")
    p.add_option('-i', '--info', dest='info', action="store_true", default=False, help='Show compiled project params and exit.')
    p.add_option('-p', '--path', dest='path', default=path, help='Path to base deploy projects dir. Required if not set SITES_HOME environment.')
    p.add_option('-b', '--branch', dest='branch', help='Project branch.', default='master')
    p.add_option('-t', '--template', dest='template', help='Config templates.')
    p.add_option('-c', '--config', dest='config', help='Config file.')
    p.add_option('-m', '--module', dest="module", help="Deploy module")
    p.add_option('-s', '--src', dest='src', help='Path to source (filesystem or repository address ex: git+http://git_adress).')

    options, args = p.parse_args()

    if not options.path or not args:
        p.print_help(sys.stdout)

    else:
        deploy( args[0], options )
