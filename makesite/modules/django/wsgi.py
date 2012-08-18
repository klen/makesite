#!/usr/bin/env python
import os

from django.core.wsgi import get_wsgi_application


os.environ['DJANGO_SETTINGS_MODULE'] = os.environ.get(
    'DJANGO_SETTINGS_MODULE', 'settings.dev')
application = get_wsgi_application()

if 'dev' in os.environ['DJANGO_SETTINGS_MODULE']:
    from werkzeug.debug import DebuggedApplication
    from django.views import debug

    def null_technical_500_response(request, exc_type, exc_value, tb):
        raise exc_type, exc_value, tb
    debug.technical_500_response = null_technical_500_response
    application = DebuggedApplication(application, evalex=True)
