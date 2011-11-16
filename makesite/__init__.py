#!/usr/bin/env python

from .settings import VERSION


version_info = map(int, VERSION.split('.'))

__version__ = version = VERSION
__project__ = PROJECT = __name__
__author__ = AUTHOR = "Kirill Klenov <horneds@gmail.com>"
__license__ = LICENSE = "GNU LGPL"
