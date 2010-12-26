from django.test.client import RequestFactory
from django.utils import unittest

from views import Index


class BaseTestCase( unittest.TestCase ):

    def setUp( self ):
        self.factory = RequestFactory()

    def test_response(self):
        request = self.factory.get('/')
        view = Index.as_view()
        response = view(request)
        self.assertEquals(response.status_code, 200)
