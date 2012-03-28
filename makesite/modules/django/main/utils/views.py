from StringIO import StringIO

from django import http
from django.core.serializers.json import Serializer
from django.db.models.query import QuerySet
from django.views.generic import TemplateView


class TemplateContextView(TemplateView):
    """ Allow define context in as_view method.
    """
    context = dict()

    def __init__(self, context=None, **kwargs):
        self.context = context or dict()
        super(TemplateContextView, self).__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        self.context.update(self.get_context_data(**kwargs))
        return self.render_to_response(self.context)


class AbstractResponseMixin(object):
    """ Abstract class for data serialize.
    """
    mimetype = "application/text"

    @staticmethod
    def render_template(context):
        "String representation of given context."
        return str(context)

    def render_to_response(self, context):
        "Return HttpResponse."
        return http.HttpResponse(
            self.render_template(context),
            content_type=self.mimetype)


class JSONResponseMixin(AbstractResponseMixin):
    """ Serialize queryset or any objects context in JSON.
    """
    mimetype = "application/json"

    def render_template(self, context):
        encoder = Serializer()
        if isinstance(context, QuerySet):
            return encoder.serialize(context, ensure_ascii=False)

        else:
            encoder.objects = context
            encoder.options = dict()
            encoder.stream = StringIO()
            encoder.end_serialization()
            return encoder.getvalue()


class JSONView(JSONResponseMixin, TemplateView):
    """ Render view context in JSON.
    """
    pass
