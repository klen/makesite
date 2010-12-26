from django.conf import settings
from django.core import signals
from django.test.client import Client, WSGIRequest, close_connection, BaseHandler, curry, store_rendered_templates, got_request_exception, TemplateDoesNotExist, signals as test_signals
from django.utils.importlib import import_module


class TestHandler(BaseHandler):
    def __call__(self, environ):

        if self._request_middleware is None:
            self.load_middleware()

        signals.request_started.send(sender=self.__class__)
        request = WSGIRequest(environ)

        # Apply request middleware
        for middleware_method in self._request_middleware:
            middleware_method(request)

        response = self.get_response(request)
        try:
            # Apply response middleware.
            for middleware_method in self._response_middleware:
                response = middleware_method(request, response)
            response = self.apply_response_fixes(request, response)

        finally:
            signals.request_finished.disconnect(close_connection)
            signals.request_finished.send(sender=self.__class__)
            signals.request_finished.connect(close_connection)

        return response, request


class TestClient(Client):
    def __init__(self, **defaults):
        super(TestClient, self).__init__(**defaults)
        self.handler = TestHandler()

    def request(self, **request):
        environ = {
            'HTTP_COOKIE':      self.cookies,
            'PATH_INFO':         '/',
            'QUERY_STRING':      '',
            'REMOTE_ADDR':       '127.0.0.1',
            'REQUEST_METHOD':    'GET',
            'SCRIPT_NAME':       '',
            'SERVER_NAME':       'testserver',
            'SERVER_PORT':       '80',
            'SERVER_PROTOCOL':   'HTTP/1.1',
            'wsgi.version':      (1,0),
            'wsgi.url_scheme':   'http',
            'wsgi.errors':       self.errors,
            'wsgi.multiprocess': True,
            'wsgi.multithread':  False,
            'wsgi.run_once':     False,
        }
        environ.update(self.defaults)
        environ.update(request)

        data = {}
        on_template_render = curry(store_rendered_templates, data)
        test_signals.template_rendered.connect(on_template_render)
        got_request_exception.connect(self.store_exc_info)

        try:
            response, request = self.handler(environ)
        except TemplateDoesNotExist, e:
            if e.args != ('500.html',):
                raise

        if self.exc_info:
            exc_info = self.exc_info
            self.exc_info = None
            raise exc_info[1], None, exc_info[2]

        response.client = self
        response.request = request

        for detail in ('template', 'context'):
            if data.get(detail):
                if len(data[detail]) == 1:
                    setattr(response, detail, data[detail][0])
                else:
                    setattr(response, detail, data[detail])
            else:
                setattr(response, detail, None)

        if response.cookies:
            self.cookies.update(response.cookies)

        return response

    def get_session(self):
        if self.session:
            return self.session

        if 'django.contrib.sessions' in settings.INSTALLED_APPS:
            engine = import_module(settings.SESSION_ENGINE)
            cookie = self.cookies.get(settings.SESSION_COOKIE_NAME, None)
            return engine.SessionStore(cookie.value) if cookie else engine.SessionStore()
        return dict()

