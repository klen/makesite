from ConfigParser import NoOptionError
from os import path as op, makedirs
from shutil import copytree
from tempfile import mkdtemp

from makesite import settings, core
from makesite.utils import OrderedSet, MakesiteConfigParser


class Engine(object):

    def __init__(self, args):
        self.args = args
        self.templates = None
        self.tmp_deploy_dir = None
        self.src_deploy_dir = None
        self.home = args.home
        self.deploy_dir = args.deploy_dir

        self.parser = MakesiteConfigParser()
        self.parser.add_section('Main')
        self.parser.set('Main', 'project', args.PROJECT)
        self.parser.set('Main', 'branch', args.branch)
        self.parser.set('Main', 'deploy_dir', self.deploy_dir)
        self.parser.set('Main', 'makesite_home', self.home)
        self.parser.read([
            settings.BASECONFIG,
            settings.HOMECONFIG,
            op.join(self.home, settings.CFGNAME),
            args.config
        ])

        self.tmp_deploy()

    def tmp_deploy(self):
        self.tmp_deploy_dir = mkdtemp()
        self.src_deploy_dir = op.join(self.tmp_deploy_dir, 'source')

        src = self.args.src or self['src']
        core.print_header('Clone src: %s' % src, '-')

        for tp, tpl in settings.SRC_TYPES:
            if src.startswith(tp + '+'):
                makedirs(self.src_deploy_dir)
                program = core.which(tp)
                assert program, '%s not found.' % tp.title()
                cmd = tpl % (program, src[len(tp) + 1:], self.src_deploy_dir)
                core.call(cmd, shell=True)
                break
        else:
            copytree(src, self.src_deploy_dir)

        self.parser.set('Main', 'src', src)
        self.parser.read(op.join(self.src_deploy_dir, settings.CFGNAME))

        self.parser.set('Templates', 'source_dir', op.join(self.src_deploy_dir))
        self.templates = OrderedSet(self.get_templates(
                ['base'] + (self.args.template or self['template']).split(',')))

        templates = ','.join(str(x[0]) for x in self.templates)
        self['template'] = templates

        core.print_header('Deploy templates: %s' % templates, sep='-')
        with open(op.join(self.tmp_deploy_dir, settings.TPLNAME), 'w') as f:
            f.write(templates)
            f.close()

        # Prepare templates
        for template, path in self.templates:
            core.prepare_template(template, path, self.parser, self.tmp_deploy_dir)

        context = dict(self.parser.items('Main'))
        with open(op.join(self.tmp_deploy_dir, settings.CFGNAME), 'w') as f:
            f.write('[Main]\n')
            f.writelines("{0:<20} = {1}\n".format(key, context[key]) for key in sorted(context.iterkeys()))
            f.close()

        if not self.args.info:
            core.print_header('Check requirements', sep='-')
            for script in core.get_scripts(self.tmp_deploy_dir, prefix='check'):
                core.call(script, shell=True)

    def get_templates(self, templates):
        for name in templates:
            try:
                path = self.parser.get('Templates', name)
            except NoOptionError:
                path = op.join(settings.TPL_DIR, name)
            assert op.exists(path), "Not found template: '%s (%s)'" % (name, path)
            tplname = op.join(path, settings.TPLNAME)
            if op.exists(tplname):
                for item in self.get_templates(open(tplname).read().strip().split(',')):
                    yield item
            yield (name, path)

    def __getitem__(self, name):
        try:
            return self.parser.get('Main', name)
        except NoOptionError:
            return None

    def __setitem__(self, name, value):
        self.parser.set('Main', name, value)
