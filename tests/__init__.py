from os import path as op
from tempfile import mkdtemp

from makesite import settings


settings.MAKESITE_HOME = op.dirname(mkdtemp())

from .common import *
from .main import *
