#!/usr/bin/env python
# coding: utf-8
import os
import bottle
from utils import get_sites

os.chdir(os.path.dirname(__file__))


@bottle.route('/')
@bottle.route('/index.html')
@bottle.view('index')
def index():
    return dict(sites=get_sites())

bottle.debug(True)
application = bottle.default_app()
