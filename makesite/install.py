from os import path as op, environ
from shutil import copytree
from tempfile import mkdtemp

from initools.configparser import NoOptionError

from . import settings
from .core import print_header, call, LOGGER, which, OrderedSet
from .site import Site


class Installer(settings.MakesiteParser):

    def __init__(self, args):
        " Load configuration. "

        super(Installer, self).__init__()

        assert args.PROJECT and args.branch and args.home

        self.args = args

        self['project'] = args.PROJECT
        self['branch'] = args.branch
        self['safe_branch'] = self['branch'].replace('/',
                                                     '-').replace(' ', '-')
        self['makesite_home'] = args.home
        self['deploy_dir'] = mkdtemp()
        call("chmod a+rwx %s" % self.deploy_dir, shell=True)

        self.read([
            settings.BASECONFIG, settings.HOMECONFIG,
            op.join(args.home, settings.CFGNAME),
            args.config
        ])

        src = args.src or self['src']
        assert src, "Not found the source. Use options '-s' or set 'src' in your ini files."
        self['src'] = src

        self.target_dir = getattr(args, 'deploy_dir', None) or op.join(
            args.home, self['project'], self['safe_branch'])
        self.templates = ['base']
        self['src_user'] = self['src_user'] or environ.get('USER')

    def clone_source(self):
        " Clone source and prepare templates "

        print_header('Clone src: %s' % self.src, '-')

        # Get source
        source_dir = self._get_source()

        # Append settings from source
        self.read(op.join(source_dir, settings.CFGNAME))

        self.templates += (self.args.template or self.template).split(',')
        self.templates = OrderedSet(self._gen_templates(self.templates))
        self['template'] = ','.join(str(x[0]) for x in self.templates)

        print_header('Deploy templates: %s' % self.template, sep='-')
        with open(op.join(self.deploy_dir, settings.TPLNAME), 'w') as f:
            f.write(self.template)

        with open(op.join(self.deploy_dir, settings.CFGNAME), 'w') as f:
            self['deploy_dir'], tmp_dir = self.target_dir, self.deploy_dir
            self.write(f)
            self['deploy_dir'] = tmp_dir

        # Create site
        site = Site(self.deploy_dir)

        # Prepare templates
        for template_name, template in self.templates:
            site.paste_template(template_name, template, tmp_dir)

        # Create site
        if self.args.info:
            print_header('Project context', sep='-')
            LOGGER.debug(site.get_info(full=True))
            return None

        # Check requirements
        call('sudo chmod +x %s/*.sh' % self.service_dir)
        site.run_check(service_dir=self.service_dir)

        # Save options
        site.write()

        return site

    def build(self):
        print_header('Build site', sep='-')
        call('sudo mkdir -p %s' % op.dirname(self.target_dir))
        call('sudo mv %s %s' % (self.deploy_dir, self.target_dir))
        call('sudo chmod 0755 %s' % self.target_dir)

    def _get_source(self):
        " Get source from CVS or filepath. "
        source_dir = op.join(self.deploy_dir, 'source')
        for tp, cmd in settings.SRC_CLONE:
            if self.src.startswith(tp + '+'):
                program = which(tp)
                assert program, '%s not found.' % tp
                cmd = cmd % dict(src=self.src[len(tp) + 1:],
                                 source_dir=source_dir,
                                 branch=self.branch)
                cmd = "sudo -u %s %s" % (self['src_user'], cmd)
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
            assert op.exists(
                path), "Not found template: '%s (%s)'" % (name, path)
            tplname = op.join(path, settings.TPLNAME)
            if op.exists(tplname):
                for item in self._gen_templates(open(tplname).read().strip().split(',')):
                    yield item
            self.read(op.join(path, settings.CFGNAME), extending=True)
            yield (name, path)
