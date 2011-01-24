from django.test.client import Client
from django.utils import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_response(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
