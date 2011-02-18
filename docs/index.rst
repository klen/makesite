.. makesite documentation master file, created by
   sphinx-quickstart on Wed Feb 16 18:28:21 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to makesite documentation!
====================================

Makesite is collection scripts for make and control site structure.


Design overview
---------------

* support wsgi projects, `django`_, `tornado`_ and etc
* projects may be isolated with `virtualenv`_;
* requirements are managed using `pip`_;
* server interactions are automated and repeatable
* easy configure
* cron, memcached, celery, compass support
* git or local path sources
* have server for browse deployed project and their setting
* contains base django, wsgi projects
* adds some useful bash commands: cdsite, lssites, updatesite, removesite, envsite and etc with bash autocomplete


Several projects can be deployed on the same VPS using makesite.
One project can be deployed on several servers. Projects are isolated and
deployments are repeatable. Project can be removed or updated in auto mode.
Makesite useful for version control system hooks or automatic make dev zones.

    .. warning ::
       Makesite needed root or sudo access on deploy project
       But dont run sudo makesite because he is dont find your $SITES_PATH settings.


Requirements
-------------

- python >= 2.5
- pip >= 0.8


Contents:
---------

.. toctree::
   :maxdepth: 2

   usage
   guide
   examples
   options
   templates
   modules

Make sure you`ve read the following document if you are upgrading from previous versions of makesite:

.. toctree::
   :maxdepth: 1

   changes

.. note::

    makesite is still at early stages of development and API may
    change in future.


Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/makesite/issues


Contributing
============

Development of makesite happens at github:
https://github.com/klen/makesite


License
=======

Licensed under a `GNU lesser general public license`_.


Related work
============

There are great projects aiming the same goal. Many of them are listed
here: http://djangopackages.com/grids/g/deployment/


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _nginx: http://www.nginx.org/
.. _supervisor: http://supervisord.org/
.. _django: http://djangoproject.com/
.. _tornado: http://www.tornadoweb.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv 
.. _pip: http://pip.openplans.org/
.. _git: http://git-scm.com/
.. _GNU lesser general public license: http://www.gnu.org/copyleft/lesser.html
