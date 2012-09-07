from os import path as op
from sys import version_info
from unittest import TestCase

from makesite.install import Installer

from makesite.site import Site, gen_sites, find_site


class CommonTest(TestCase):

    def test_site(self):
        from makesite import settings

        args = FakeArgs(
            template='django',
            branch='feature/red-alert',
            home=settings.MAKESITE_HOME,
            src=op.join(settings.MOD_DIR, 'django'),
        )

        # Init engine
        engine = Installer(args)
        self.assertTrue(op.isdir(engine.deploy_dir))
        self.assertEqual(engine.templates, ['base'])

        # Clone source
        engine.clone_source()
        self.assertTrue(op.isdir(op.join(engine.deploy_dir, 'source')))
        self.assertTrue(
            op.isfile(op.join(engine.deploy_dir, 'source', 'Makefile')))
        self.assertEqual(engine.template, 'base,src-dir,virtualenv,django')
        self.assertEqual(engine.target_dir, op.join(
            args.home, args.PROJECT, args.branch.replace('/', '-')))
        self.assertEqual(engine.django_settings, 'settings.dev')
        self.assertEqual(engine.templates, [
            ('base', op.join(settings.TPL_DIR, 'base')),
            ('src-dir', op.join(settings.TPL_DIR, 'src-dir')),
            ('virtualenv', op.join(settings.TPL_DIR, 'virtualenv')),
            ('django', op.join(settings.TPL_DIR, 'django')),
        ])
        self.assertTrue(
            op.isfile(op.join(engine.deploy_dir, settings.TPLNAME)))
        self.assertTrue(op.isfile(
            op.join(engine.deploy_dir, 'service', 'django_install.sh')))
        self.assertTrue(
            op.isfile(op.join(engine.deploy_dir, settings.CFGNAME)))

        # Build site
        engine.build()

        # Init site
        site = Site(engine.target_dir)
        self.assertEqual(site.get_name(), u'main.feature-red-alert')
        self.assertEqual(site.get_info(
        ), u'main.feature-red-alert [base,src-dir,virtualenv,django]')
        self.assertTrue('www-data' in site.get_info(full=True))

        if version_info >= (2, 7):
            with self.assertRaises(AssertionError):
                site.add_template('django')

        self.assertEqual(site._get_template_path(
            'zeta'), op.join(settings.TPL_DIR, 'zeta'))
        site.add_template('zeta')
        site.run_install('zeta')
        zeta_scripts = list(site._gen_scripts('install', template_name='zeta'))
        self.assertEqual(zeta_scripts, [u'/tmp/main/feature-red-alert/service/zeta_install_update.sh'])
        self.assertEqual(site.get_info(), u'main.feature-red-alert [base,src-dir,virtualenv,django,zeta]')

        self.assertEqual(site['safe_branch'], 'feature-red-alert')

        site.remove_template('zeta')
        site.run_remove('zeta')
        self.assertEqual(site.get_info(
        ), u'main.feature-red-alert [base,src-dir,virtualenv,django]')

        # Find site
        self.assertTrue(find_site(site.deploy_dir))
        self.assertTrue(find_site(site.get_name()))

        # Gen scripts
        self.assertTrue(op.join(site.service_dir,
                        'django_install.sh') in site._gen_scripts('install'))

        sites = list(gen_sites(op.dirname(engine.deploy_dir)))
        self.assertTrue(sites)
        for s in sites:
            s.clean()


class FakeArgs(dict):

    def __init__(self, **kwargs):
        defaults = dict(
            template='',
            PROJECT='main',
            branch='master',
            config='')
        defaults.update(kwargs)

        super(FakeArgs, self).__init__(**defaults)

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value


class RemoteTest(TestCase):
    def test_host_params(self):
        from makesite import settings, remote

        self.assertEqual(
            remote.host_params('site.com'), (settings.USER, 'site.com'))
        self.assertEqual(
            remote.host_params('master@site.com'), ('master', 'site.com'))
