import hashlib
import logging
import re

from django.core.cache import cache
from django.db.models import Model, get_model
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.utils.encoding import smart_str


LOG = logging.getLogger('cache')


def cached_instance(model, timeout=None, **filters):
    """ Auto cached model instance.
    """
    if isinstance(model, basestring):
        model = _str_to_model(model)

    cache_key = generate_cache_key(model, **filters)
    return get_cached(cache_key, model.objects.select_related().get, kwargs=filters)


def cached_query(qs, timeout=None):
    """ Auto cached queryset and generate results.
    """
    cache_key = generate_cache_key(qs)
    return get_cached(cache_key, list, args=(qs,), timeout=None)


def clean_cache(cached, **kwargs):
    " Generate cache key and clean cached value. "

    if isinstance(cached, basestring):
        cached = _str_to_model(cached)

    cache_key = generate_cache_key(cached, **kwargs)
    cache.delete(cache_key)


def generate_cache_key(cached, **kwargs):
    """ Auto generate cache key for model or queryset
    """

    if isinstance(cached, QuerySet):
        key = str(cached.query)

    elif isinstance(cached, (Model, ModelBase)):
        key = '%s.%s:%s' % (cached._meta.app_label,
                            cached._meta.module_name,
                            ','.join('%s=%s' % item for item in kwargs.iteritems()))

    else:
        raise AttributeError("Objects must be queryset or model.")

    if not key:
        raise Exception('Cache key cannot be empty.')

    key = clean_cache_key(key)
    return key


def clean_cache_key(key):
    """ Replace spaces with '-' and hash if length is greater than 250.
    """
    cache_key = re.sub(r'\s+', '-', key)
    cache_key = smart_str(cache_key)

    if len(cache_key) > 200:
        cache_key = cache_key[:150] + '-' + hashlib.md5(cache_key).hexdigest()

    return cache_key


def get_cached(cache_key, func, timeout=None, args=None, kwargs=None):
    args = args or list()
    kwargs = kwargs or dict()
    result = cache.get(cache_key)

    if result is None:

        if timeout is None:
            timeout = cache.default_timeout

        result = func(*args, **kwargs)
        cache.set(cache_key, result, timeout=timeout)

    return result


def _str_to_model(string):
    assert '.' in string, ("'model_class' must be either a model"
                           " or a model name in the format"
                           " app_label.model_name")
    app_label, model_name = string.split(".")
    return get_model(app_label, model_name)
