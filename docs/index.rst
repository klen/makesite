.. makesite documentation master file, created by
   sphinx-quickstart on Wed Feb 16 18:28:21 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

======================
Makesite documentation
======================

**Makesite** is the system for deploying and managing sites.


Features
--------

* support wsgi projects, `django`_, `tornado`_ and etc;
* projects may be isolated with `virtualenv`_;
* requirements are managed using `pip`_;
* server interactions are automated and repeatable;
* easy configured and expanded;
* cron, memcached, celery, compass, zeta support;
* git or local path sources;
* contains base standart django, wsgi projects for fast start;
* includes a server for a list of projects and installations;
* adds to bash a some useful commands:
  cdsite, lssites, updatesite, removesite, envsite, worksite with bash autocomplete

Several projects can be deployed on the same VPS using ``makesite``.
One project can be deployed on several servers. Projects are isolated and
deployments are repeatable. Project can be removed or updated in auto mode.
Makesite is useful for version control system hooks or fast automatically creating dev zones.
I use it for production deployment, too.

    .. warning ::
       Makesite needed root or sudo access on deploy project.
       But do not run it under sudo because he did not find your :envvar:`SITES_HOME` settings.
       He asks access in process.

    .. warning ::
       Some templates makesite install missing software automaticaly ( nginx, supervisor ).
       Look to the templates before deploy.


Requirements
-------------

- Ubuntu and Debian based systems.
  But it can run other nix systems.
- python >= 2.5
- pip >= 0.8


Meeting
-------

.. toctree::
   :maxdepth: 1

   introduction
   examples


Digging in
-----------

.. toctree::
   :maxdepth: 2

   usage
   configuration
   templates
   modules
   customization

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

**Feedback are welcome!**

.. _nginx: http://www.nginx.org/
.. _supervisor: http://supervisord.org/
.. _django: http://djangoproject.com/
.. _tornado: http://www.tornadoweb.org/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv 
.. _pip: http://pip.openplans.org/
.. _git: http://git-scm.com/
.. _GNU lesser general public license: http://www.gnu.org/copyleft/lesser.html
