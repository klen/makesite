Templates
=========

**Template** in makesite - sctructure of files and folders. It will be copied when makesite install project.
Files in template, parse with makesite options. Service files in template will be launched.


.. contents::


Standart templates
==================

base
----

base_ template. Auto added to all makesite projects. Load project source and create base structure. `base source`_

#. **INSTALL**, **UPDATE**

   Change deploy dir owner and group to makesite option <site_user>:<site_group>, default is www-data

   Make service files is executable.


src-dir
-------

src-dir_ template for update code in project from source. This template will be auto added in project if deploy source it is local path. `src-dir source`_

#. **UPDATE**

   Copy project source from source dir to deploy source dir

   Copy static dir from deploy source static dir to deploy static dir


src-git
-------

src-git_ template for update code in project from git_ source. This template will be auto added in project if deploy source it is git path. `src-git source`_

#. **UPDATE**

   Update git project source dir.


db-postgres
-----------

db-postgres_ template for auto create user and db for project if it not exist. `db-postgres source`_

    .. note ::

        Require <pguser>, <pghost>, <pgpassword> variables in configs with admin rights

#. **INSTALL**

   Create postgres user <dbuser> if not exists, default is <project> with password <dbpassword> default is <project>

   Create postgres db <dbname> default <project>_master


django
------

django_ template for deploy and update django projects. `django source`_

    .. note ::
        Now it working in last django version from trunk `collectstatic`
        Required manage.py in project root.

**INCLUDED** memcached_, virtualenv_, cron_

#. **INSTALL**

   Run manage.py syncdb

#. **UPDATE**

   Run manage.py migrate
   Run manage.py collectstatic


tornado
-------

Template fir deploy and update tornado projects. Contains nginx and supervisor configs. `tornado source`_

    .. note ::
        Required app.py in project root with tornado application
        app.py must parse --port option

**INCLUDED** virtualenv_, cron_, memcached_, supervisor_, nginx_


memcached
---------

memcached_ template for install python-memcached and flush memcached cache on updates. `memcached source`_

    .. note ::
        Default memcached_host=localhost, memcached_port=11211

#. **INSTALL**, **UPDATE**

   Install python-memcached if not exist and flush memcached cache


virtualenv
----------

Template for create virtual env for project and update pip requirements.

    .. note ::
        Default file for pip requirements `requirements.txt` in project source root

#. **INSTALL**
   Install virtualenv in it not exists.
   Create virtual env and update pip requirements

#. **UPDATE**
   Update pip requirements if it needed


cron
----

Template for add project cron tasks in crond. `cron source`_ 

    .. note ::
        Default <cron_projectfile> is crontab in project root. File in cron format.
        Commands from this file will be runned from <site_user> relative project root
        and with enabled project virtualenv

#. **INSTALL**, **UPDATE**

   Parse project crontab file and add it to cron.

#. **REMOVE**

   Remove project cron tasks from cron.


nginx
-----

nginx_ template for nginx support.

    .. note ::

        Default nginx configs path <nginx_confpath>: /etc/nginx/sites-enabled/{{ project }}.{{ branch }}.conf 

#. **INSTALL**

   Install nginx if not exist

   Create link <nginx_confpath> to deploy nginx.conf ( its make other templates ex django or tornado )

   Restart nginx

#. **REMOVE**

   Remove link <nginx_confpath>

   Restart nginx


supervisor
----------

supervisor_ template for supervisor support.

   .. note ::

       Default supervisor configs path <supervisor_confpath>: /etc/supervisor/conf.d/{{ project }}.{{ branch }}.conf


#. **INSTALL**

   Install supervisor if not exists

   Create link to <supervisor_confpath> its make another templates ex: django, tornado

   Reread supervisor configs

#. **UPDATE**

   Restart supervisor project task

#. **REMOVE**

   Remove link <supervisor_confpath>

   Reread supervisor configs


uwsgi
-----

uwsgi_ for uwsgi support. Contains nginx and supervisor configs. `uwsgi source`_

    .. note ::
        uwsgi template waiting for wsgi.py in project source root with defined wsgi application


zeta
----

Template for packing project static files. `zeta source`_

#. **INSTALL**, **UPDATE**
   Packing js, css, scss files from deploy static dir.


compass
-------

Tempalate for compass support. `compass source`_



**INCLUDED** nginx_ and supervisor_ templates.


.. _base source: https://github.com/klen/makesite/tree/master/makesite/base
.. _src-dir source: https://github.com/klen/makesite/tree/master/makesite/templates/src-dir
.. _src-git source: https://github.com/klen/makesite/tree/master/makesite/templates/src-git
.. _db-postgres source: https://github.com/klen/makesite/tree/master/makesite/templates/db-postgres
.. _memcached source: https://github.com/klen/makesite/tree/master/makesite/templates/memcached
.. _nginx source: https://github.com/klen/makesite/tree/master/makesite/templates/nginx
.. _supervisor source: https://github.com/klen/makesite/tree/master/makesite/templates/supervisor
.. _uwsgi source: https://github.com/klen/makesite/tree/master/makesite/templates/uwsgi
.. _django source: https://github.com/klen/makesite/tree/master/makesite/templates/django
.. _tornado source: https://github.com/klen/makesite/tree/master/makesite/templates/tornado
.. _zeta source: https://github.com/klen/makesite/tree/master/makesite/templates/zeta
.. _virtualenv source: https://github.com/klen/makesite/tree/master/makesite/templates/virtualenv
.. _cron source: https://github.com/klen/makesite/tree/master/makesite/templates/cron
.. _compass source: https://github.com/klen/makesite/tree/master/makesite/templates/compass

.. _git: http://git-scm.com/
