from os import path as op, listdir, makedirs, remove
from shutil import copy2
from tempfile import mkdtemp

from tempita import Template

from makesite import settings
from makesite.core import walklevel, call, print_header, is_exe, MakesiteParser, Error, \
        gen_template_files, LOGGER


class Site(MakesiteParser):

    def __init__(self, deploy_dir):
        super(Site, self).__init__()

        self.deploy_dir = deploy_dir.rstrip(op.sep)
        self.read([op.join(self.deploy_dir, settings.CFGNAME)])
        assert self.project and self.branch, "Invalid site: %s" % self.deploy_dir
        self.templates = self.template.split(',')

    def get_info(self, full=False):
        if full:
            context = self.as_dict()
            return "".join("{0:<25} = {1}\n".format(
                    key, context[key]) for key in sorted(context.iterkeys()))
        return "%s [%s]" % (self.get_name(), self.template)

    def get_name(self):
        return "%s.%s" % (self.project, self.branch)

    def run_check(self, template_name=None, service_dir=None):
        print_header('Check requirements', sep='-')
        map(call, self._gen_scripts('check', template_name=template_name, service_dir=service_dir))
        return True

    def run_install(self, template_name=None, service_dir=None):
        print_header('Install %s' % self.get_name())
        map(call, self._gen_scripts('install', template_name=template_name, service_dir=service_dir))
        return True

    def run_update(self, template_name=None, service_dir=None):
        print_header('Update %s' % self.get_name())
        map(call, self._gen_scripts('update', template_name=template_name, service_dir=service_dir))
        return True

    def run_remove(self, template_name=None, service_dir=None):
        print_header('Uninstall %s' % self.get_name())
        map(call, self._gen_scripts('remove', template_name=template_name, service_dir=service_dir))
        return True

    def paste_template(self, template_name, template=None, deploy_dir=None):
        " Paste template. "

        LOGGER.info("Paste template: %s" % template_name)
        deploy_dir = deploy_dir or self.deploy_dir
        template = template or self._get_template_path(template_name)
        self.read([op.join(template, settings.CFGNAME)], extending=True)

        for fname in gen_template_files(template):
            curdir = op.join(deploy_dir, op.dirname(fname))
            if not op.exists(curdir):
                makedirs(curdir)

            source = op.join(template, fname)
            target = op.join(deploy_dir, fname)
            copy2(source, target)
            name, ext = op.splitext(fname)
            if ext == '.tmpl':
                t = Template.from_filename(target, namespace=self.as_dict())
                with open(op.join(deploy_dir, name), 'w') as f:
                    f.write(t.substitute())
                remove(target)

        return deploy_dir

    def add_template(self, template_name):
        assert not template_name in self.templates, "Template already installed."
        print_header("Append template: %s" % template_name)
        deploy_tmpdir = mkdtemp()
        self.paste_template(template_name, deploy_dir=deploy_tmpdir)
        call('sudo cp -r %s/* %s' % (deploy_tmpdir, self.deploy_dir))
        call('sudo chown %s:%s %s' % (self.site_user, self.site_group, self.deploy_dir))
        self.templates.append(template_name)
        self['template'] = ','.join(self.templates)
        self.write()

    def remove_template(self, template_name):
        assert template_name in self.templates, "Template not installed."
        print_header("Remove template: %s" % template_name)
        template = self._get_template_path(template_name)
        if not template.startswith(self.source_dir):
            for f in gen_template_files(template):
                call('sudo rm -f %s' % op.join(self.deploy_dir, f))
        self.templates = filter(lambda x: x != template_name, self.templates)
        self['template'] = ','.join(self.templates)
        self.write()

    def write(self, deploy_dir=None):
        deploy_dir = deploy_dir or self.deploy_dir
        with open(op.join(deploy_dir, settings.CFGNAME), 'w') as f:
            super(Site, self).write(f)

    def clean(self):
        print_header('Delete %s' % self.get_name(), sep="-")
        call('sudo rm -rf %s' % self.deploy_dir)

    def _gen_scripts(self, prefix, service_dir=None, template_name=None):
        service_dir = service_dir or self.service_dir or op.join(self.deploy_dir, 'service')
        files = sorted(listdir(service_dir))
        for template in self.templates:
            for f in files:
                if template_name and not f.startswith("%s_" % template_name):
                    continue

                path = op.join(service_dir, f)
                if f.startswith(template) and (not prefix or prefix in f) and is_exe(path):
                    yield path

    def _get_template_path(self, template_name):
        try:
            path = self.get('Templates', template_name)
        except Error:
            path = op.join(settings.TPL_DIR, template_name)
        assert op.exists(path), "Template not found."
        return path


def gen_sites(path):
    for root, _, _ in walklevel(path, 2):
        try:
            yield Site(root)
        except AssertionError:
            continue


def find_site(path):
    " Find site by path or name. "

    try:
        return Site(path)
    except AssertionError:
        if not settings.MAKESITE_HOME or op.sep in path:
            raise

        path = path if '.' in path else "%s.master" % path
        project, branch = path.split('.', 2)
        return Site(op.join(settings.MAKESITE_HOME, project, branch))
