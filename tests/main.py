from unittest import TestCase


class MainTest(TestCase):

    def test_main(self):
        from makesite import main

        main.install(['test', '-m', 'static'])
        main.install(['test', '-m', 'static', '-i'])
        site = main.install(['test', '-m', 'static', '-r'])
        self.assertTrue(site)
        main.info(['test'])
        main.ls([])
        main.update(['test'])
        main.uninstall([site.deploy_dir])

    def test_custom(self):
        from makesite import main
        from os import path as op

        site = main.install(['custom_test', '-s', op.abspath(op.join(op.dirname(__file__), 'custom'))])
        self.assertTrue(site)
        main.uninstall([site['deploy_dir']])
