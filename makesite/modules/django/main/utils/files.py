from hashlib import md5
from os import path
from time import time


def upload_to(instance, filename):
    """ Auto upload function for File and Image fields.
    """
    ext = path.splitext(filename)[1]
    name = str(instance.pk or time()) + filename

    # We think that we use utf8 based OS file system
    filename = md5(name.encode('utf8')).hexdigest() + ext
    return path.join(
        instance._meta.app_label,
        instance._meta.module_name,
        filename[:2],
        filename[2:4],
        filename)
