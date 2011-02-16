.. makesite documentation master file, created by
   sphinx-quickstart on Wed Feb 16 18:28:21 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to makesite documentation!
====================================

Makesite is collection scripts for make and control site structure.


Design overview
---------------

* support wsgi projects, django, tornado and etc
* projects may be isolated with `virtualenv`_;
* requirements are managed using `pip`_;
* server interactions are automated and repeatable
* easy configure
* cron, memcached, celery, compass support
* git or local path sources
* have server for browse deployed project and their setting
* contains base django, wsgi projects
* add some useful bsh commands: cdsite, lssites, updatesite, removesite, envsite and etc with bash autocomplete


Contents:

.. toctree::
   :maxdepth: 2

   templates
   related


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

