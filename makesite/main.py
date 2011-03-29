#!/usr/bin/env python
import ConfigParser, os, sys, subprocess

import argparse

from makesite import version, INI_FILENAME, TEMPLATES_FILE
from makesite.template import Template


BASEDIR = os.path.realpath(os.path.dirname(__file__))
BASE_TEMPLATES_DIR = os.path.join(BASEDIR, 'templates')
MODULES_DIR = os.path.join(BASEDIR, 'modules')

PATH_VARNAME = 'SITES_HOME'

BASECONFIG = os.path.join( BASEDIR, INI_FILENAME )
HOMECONFIG = os.path.join( os.getenv('HOME'), INI_FILENAME )

PYTHON_PREFIX = 'python' + '.'.join( str(x) for x in sys.version_info[:2] )


def deploy(options):
    """ Deploy project.
    """
    # This not work in virtual env
    if os.environ.has_key('VIRTUAL_ENV'):
        print >> sys.stderr, "Please deactivate virtualenv '%s' first." % os.environ['VIRTUAL_ENV']
        sys.exit(1)

    if options.append:
        append_template(options)
        sys.exit()

    # Compile project options
    options = load_config(options)

    # Exit if requested only info
    if options['Main']['info']:
        print format_options(options['Main'])
        sys.exit()
    del options['Main']['info']

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
    templates = parse_templates(templates, options)
    options['Main']['template'] = ' '.join([t[0] for t in templates ])

    # Show project options
    print  "\nDeploy branch '%(branch)s' in project '%(project)s'\n" % options['Main']

    # Deploy templates
    for template, path in templates:
        if template != 'base':
            deploy_template(path, options, template)

    # Create makesite project files
    create_file(os.path.join( options['Main'][ 'deploy_dir' ], TEMPLATES_FILE ), ' '.join([t[0] for t in templates]))

    # Save used options
    create_file(os.path.join(options['Main']['deploy_dir'], INI_FILENAME), "[Main]\n%s" % format_options(options['Main']))

    # Run install site
    subprocess.check_call('makesiteparse %(deploy_dir)s install' % options['Main'], shell=True)


def format_options(main_options):
    """ Return string with sorted and formated options list.
    """
    keys = main_options.keys()
    keys.sort()
    return ' \n'.join(["{0:<20} = {1}".format(key, main_options[key]) for key in keys])


def load_config(options):
    """ Load config files.
    """
    # Deploy projects dir
    projects_dir = os.path.join(os.path.abspath(options.path), INI_FILENAME)

    # Load config in this order
    result = dict(Main = dict(
        project = options.project,
        python_prefix = PYTHON_PREFIX,
        branch = options.branch,
        deploy_dir = os.path.join( os.path.abspath( options.path ), options.project, options.branch ),
        info = options.info,
        sites_home = options.path,
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

        deploy_template(os.path.join(BASE_TEMPLATES_DIR, 'base'), options, 'base')
        try:
            subprocess.check_call('sh %s/%s_init.sh' % (options['Main']['project_servicedir'], template), shell=True)
        except subprocess.CalledProcessError:
            subprocess.check_call('sudo rm -rf %s' % options['Main']['deploy_dir'], shell=True)
            print >> sys.stderr, "Error deploy src: %s" % options['Main']['src']
            sys.exit(1)

        parse_config(os.path.join( options['Main']['project_sourcedir'], INI_FILENAME ), options)
        return [ 'base', template ]

    deploy_template(os.path.join(BASE_TEMPLATES_DIR, 'base'), options, 'base')
    return [ 'base' ]


def parse_config(path, result=None, replace=True):
    """ Parse config file.
    """
    parser = ConfigParser.RawConfigParser()
    parser.read(path)

    if not result:
        result = dict()

    for section in parser.sections():
        if not result.has_key( section ):
            result[ section ] = dict()

        data = dict(parser.items( section ))

        # Parse options template
        for k, v in data.items():
            if result[section].has_key(k) and not replace:
                continue

            result[section][k] = Template.sub(v, **result['Main'])

    return result


def parse_templates(templates, options):
    """ Parse templates hierarchy.
    """
    result = list()

    for template in templates:
        path = options['Templates'][template] if options.has_key('Templates') and options['Templates'].has_key(template) \
                else os.path.join(BASE_TEMPLATES_DIR, template)
        if not os.path.exists(path):
            print >> sys.stderr, "Template '%s' not found in base and custom templates." % template
            sys.exit(1)

        try:
            f = open( os.path.join(path, TEMPLATES_FILE ), 'r')
            child = f.read().strip()
            result += parse_templates(child.split(' '), options)
        except IOError:
            pass

        result.append((template, path))

    return result


def deploy_template(path, options, template):
    """ Deploy template.
    """
    print "Deploy template '%s'." % template
    options = parse_config(os.path.join(path, INI_FILENAME), options, replace=False)

    for root, dirs, files in os.walk(path):
        dirs = root[len(path) + 1:].split(os.sep)[0]
        curdir = os.path.join(options['Main']['deploy_dir'], dirs)
        options['Main']['curdir'] = curdir
        create_dir(curdir)

        for filename in files:

            # Skip makesite config files
            if filename in (TEMPLATES_FILE, INI_FILENAME):
                continue

            # Files from bin folders copied as-is
            if dirs == 'bin':
                src = open(os.path.join( root, filename), 'rb').read()

            else:
                src = Template(filename=os.path.join(root, filename))(**options['Main'])

            create_file(os.path.join(curdir, filename), src)

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
        pid = os.getpid()
        open('/tmp/makesite_%s.tmp' % pid, 'wb').write(s)
        subprocess.check_call('sudo mv /tmp/makesite_%s.tmp %s' % (pid, path), shell=True)
        print "Create file '%s'" % path
    except subprocess.CalledProcessError:
        print 'Failed create file %s.' % path


def append_template(options):
    """ Append template to existent project.
    """
    deploy_dir = os.path.join(os.path.abspath( options.path ), options.project, options.branch)
    print  "\nAppend template '%(template)s' in project '%(project)s'\n" % vars(options)
    if not os.path.exists(deploy_dir):
        print >> sys.stderr, "\nPath %s not exists. Stop append." % deploy_dir
        sys.exit(1)
    ini_path = os.path.join(deploy_dir, INI_FILENAME)
    template_path = os.path.join(deploy_dir, TEMPLATES_FILE)
    site_options = parse_config(ini_path)
    append_templates = parse_templates(options.template.split(','), site_options)

    for template, path in append_templates:
        if template in site_options['Main']['template']:
            print >> sys.stderr, "\nTemplate %s already exists. Stop append." % template
            sys.exit(1)
        deploy_template(path, site_options, template)

    site_options['Main']['template'] += ' ' + ' '.join(t[0] for t in append_templates)

    # Update config files
    create_file(template_path, site_options['Main']['template'])
    create_file(ini_path, "[Main]\n%s" % format_options(site_options['Main']))


def main():
    """ Parse arguments and do work.
    """
    path = os.environ[ PATH_VARNAME ] if os.environ.has_key( PATH_VARNAME ) else None
    parser = argparse.ArgumentParser(
        description = "'Makesite' is scripts collection for create base project dirs and config files.",
        epilog = "See also next utilities: installsite, updatesite, removesite, cdsite, worksite, lssites, statsites."
    )

    parser.add_argument('project', help="Project name")

    if not path:
        parser.add_argument('-p', '--path', required=True, help='Path to base deploy projects dir. Required if not set SITES_HOME environment.')

    parser.add_argument('-i', '--info', action="store_true", default=False, help='Show compiled project params and exit.')
    parser.add_argument('-b', '--branch', help='Project branch.', default='master')
    parser.add_argument('-t', '--template', help='Config templates.')
    parser.add_argument('-a', '--append', action="store_true", default=False, help='Append template to exists project.')
    parser.add_argument('-c', '--config', help='Config file.')
    parser.add_argument('-m', '--module', help="Deploy module")
    parser.add_argument('-s', '--src', help='Path to source (filesystem or repository address ex: git+http://git_adress).')
    parser.add_argument('-v', '--version', action='version', version=version, help='Show makesite version')

    # Show must go on
    args = parser.parse_args()
    args.path = path if path else args.path
    deploy(args)
