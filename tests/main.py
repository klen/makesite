from unittest import TestCase

from makesite import main


class MainTest(TestCase):

    def test_main(self):
        main.install(['test', '-m', 'static'])
        main.install(['test', '-m', 'static', '-i'])
        site = main.install(['test', '-m', 'static', '-r'])
        self.assertTrue(site)
        main.ls([])
        main.uninstall([site.deploy_dir])
