import unittest
from os import path as op, listdir

from makesite import settings, main


class TestTemplates(unittest.TestCase):

    @staticmethod
    def list_dirs(dirpath):
        return sorted(filter(
                lambda x: op.isdir(op.join(dirpath, x)),
                listdir(dirpath)
            ))

    def test_templates(self):
        templates = self.list_dirs(settings.TPL_DIR)
        self.assertTrue('base' in templates)
        self.assertTrue('nginx' in templates)

        templates = ','.join(templates)
        main.install(['test', '-m', 'wsgi', '-t', templates, '-i'])
