from os import path as op, makedirs
from shutil import copytree
from tempfile import mkdtemp

from initools.configparser import NoOptionError

from makesite import settings
from makesite.core import MakesiteParser, print_header, call, LOGGER, which, OrderedSet
from makesite.site import Site


class Installer(MakesiteParser):

    def __init__(self, args):
        " Load configuration. "

        super(Installer, self).__init__()

        assert args.PROJECT and args.branch and args.home

        self.args = args

        self['project'] = args.PROJECT
        self['branch'] = args.branch
        self['makesite_home'] = args.home
        self['deploy_dir'] = args.deploy_dir or op.join(args.home, args.PROJECT, args.branch)
        self.read([
            settings.BASECONFIG, settings.HOMECONFIG,
            op.join(args.home, settings.CFGNAME),
            args.config
        ])

        self['src'] = args.src or self['src']

        self.deploy_tmpdir = mkdtemp()
        self.templates = filter(None, ['base'])

    def clone_source(self):
        " Clone source and prepare templates "

        print_header('Clone src: %s' % self.src, '-')

        source_dir = self._get_source()

        self.read(op.join(source_dir, settings.CFGNAME))

        self.templates += (self.args.template or self.template).split(',')
        self.templates = OrderedSet(self._gen_templates(self.templates))
        self['template'] = ','.join(str(x[0]) for x in self.templates)

        print_header('Deploy templates: %s' % self.template, sep='-')
        with open(op.join(self.deploy_tmpdir, settings.TPLNAME), 'w') as f:
            f.write(self.template)

        with open(op.join(self.deploy_tmpdir, settings.CFGNAME), 'w') as f:
            self.write(f)

        # Create site
        site = Site(self.deploy_tmpdir)

        # Prepare templates
        for template_name, template in self.templates:
            site.paste_template(template_name, template, self.deploy_tmpdir)

        # Create site
        if self.args.info:
            print_header('Project context', sep='-')
            LOGGER.info(site.get_info(full=True))
            return None

        # Save options
        site.write(self.deploy_tmpdir)

        # Check requirements
        site['service_dir'] = op.join(self.deploy_tmpdir, 'service')
        call('sudo chmod +x %s/*.sh' % site.service_dir)
        site.run_check()
        site['service_dir'] = op.join(self.deploy_dir, 'service')
        return site

    def build(self):
        print_header('Build site', sep='-')
        call('sudo mkdir -p %s' % op.dirname(self.deploy_dir))
        call('sudo mv %s %s' % (self.deploy_tmpdir, self.deploy_dir))
        call('sudo chmod 0755 %s' % self.deploy_dir)

    def _get_source(self):
        " Get source from CVS or filepath. "

        source_dir = op.join(self.deploy_tmpdir, 'source')
        for tp, cmd in settings.SRC_CLONE:
            if self.src.startswith(tp + '+'):
                makedirs(source_dir)
                program = which(tp)
                assert program, '%s not found.' % tp
                cmd = cmd % (self.src[len(tp) + 1:], self.deploy_tmpdir)
                call(cmd, shell=True)
                self.templates.append('src-%s' % tp)
                break
        else:
            self.templates.append('src-dir')
            copytree(self.src, source_dir)

        return source_dir

    def _gen_templates(self, templates):
        for name in templates:
            try:
                path = self.get('Templates', name)
            except NoOptionError:
                path = op.join(settings.TPL_DIR, name)
            assert op.exists(path), "Not found template: '%s (%s)'" % (name, path)
            tplname = op.join(path, settings.TPLNAME)
            if op.exists(tplname):
                for item in self._gen_templates(open(tplname).read().strip().split(',')):
                    yield item
            yield (name, path)
