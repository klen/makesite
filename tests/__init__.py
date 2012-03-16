from makesite import settings
from os import path as op


settings.MAKESITE_HOME = op.abspath(op.dirname(__file__))
