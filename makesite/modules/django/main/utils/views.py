from StringIO import StringIO

from django import http
from django.core.serializers.json import Serializer
from django.db.models.query import QuerySet
from django.views.generic import TemplateView


class TemplateContextView( TemplateView ):
    """ Allow define context in as_view method.
    """
    context = dict()

    def __init__( self, context=None, **kwargs ):
        self.context = context or dict()
        super( TemplateContextView, self ).__init__( **kwargs )

    def get(self, request, *args, **kwargs):
        self.context.update(self.get_context_data(**kwargs))
        return self.render_to_response(self.context)


class AbstractEncoderMixin( object ):
    """ Abstract class for data serialize.
    """
    mimetype = "application/text"

    def encode( self, context ):
        raise NotImplementedError()

    def render_template(self, context):
        return self.encode(context)

    def render_to_response(self, context):
        return self.get_response(self.render_template(context))

    def get_response(self, content, **httpresponse_kwargs):
        httpresponse_kwargs.update({ 'mimetype': self.mimetype })
        return http.HttpResponse(content, **httpresponse_kwargs)


class JSONViewMixin( AbstractEncoderMixin ):
    """ Serialize queryset or any objects context in JSON.
    """
    mimetype = "application/json"

    def encode( self, context ):
        encoder = Serializer()
        if isinstance(context, QuerySet):
            return encoder.serialize(context, ensure_ascii=False)
        else:
            encoder.objects = context
            encoder.options = dict()
            encoder.stream = StringIO()
            encoder.end_serialization()
            return encoder.getvalue()


class JSONView( JSONViewMixin, TemplateContextView):
    """ Render view context in JSON.
    """
    def get_context_data( self, **kwargs ):
        raise NotImplementedError()


