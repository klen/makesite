from django.views.generic import TemplateView


class Index(TemplateView):
    """ Example view.
    """
    template_name = 'main/index.html'
