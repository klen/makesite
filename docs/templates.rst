Templates
=========

**Template** in makesite - sctructure of files and folders. It will be copied when makesite install project.
Files in template, parse with makesite options. Service files in template will be launched.


Template syntax
---------------

In template files you can use simple syntax. ::

    listen      {{ port }};
    server_name {{ domain }};
    access_log  {{ deploy_dir }}/logs/nginx_access.log;
    error_log   {{ deploy_dir }}/logs/nginx_error.log;

Variable context from config and command line options. Each file from template will be processed.


List
----

:term:`base`, :term:`src-dir`, :term:`src-git`, :term:`db-postgres`, :term:`django`,
:term:`tornado`, :term:`memcached`, :term:`cron`, :term:`nginx`, :term:`supervisor`,  
:term:`uwsgi`, :term:`zeta`, :term:`compass`, :term:`html`


.. glossary::

    base
        Auto added to all makesite projects. Load project source and create base structure. `base source`_

        #. **INSTALL**, **UPDATE**

           Change deploy folder owner and group to makesite option <site_user>:<site_group>, default is www-data

           Make service files is executable.


    src-dir
        Load code in project from path.

        This template will be auto added in project if deploy source it is local path. `src-dir source`_

        #. **UPDATE**

           Copy project source from source dir to deploy source dir

           Copy static dir from deploy source static dir to deploy static dir


    src-git
        Load code in project from git_ source.

        This template will be auto added in project if deploy source it is git path. `src-git source`_

        #. **UPDATE**

           Update git project source dir.


    db-postgres
        Auto create user and db for project if it not exist. `db-postgres source`_
        .. note ::

            Require <pguser>, <pghost>, <pgpassword>, <pgport> variables in configs with admin rights

        #. **INSTALL**

           Create postgres user <dbuser> if not exists, default is <project> with password <dbpassword> default is <project>

           Create postgres db <dbname> default <project>_master.


    django
        Deploy and update django projects. `django source`_

        .. note ::
           Now it working in last django version from trunk `collectstatic`
           Required manage.py in project root.

        **INCLUDED** :term:`memcached`, :term:`virtualenv`, :term:`cron`

        #. **INSTALL**

           Run manage.py syncdb

        #. **UPDATE**

           Run manage.py migrate
           Run manage.py collectstatic


    tornado
        Deploy and update tornado projects. Contains nginx and supervisor configs. `tornado source`_

        .. note ::
           Required app.py in project root with tornado application
           app.py must parse --port option

        **INCLUDED** :term:`virtualenv`, :term:`cron`, :term:`memcached`, :term:`supervisor`, :term:`nginx`


    memcached
        Install python-memcached and flush memcached cache on updates. `memcached source`_

        **default options** ::

            memcached_host=localhost
            memcached_port=11211

        #. **INSTALL**, **UPDATE**

           Install python-memcached if not exist and flush memcached cache


    virtualenv
        Create virtual env for project and update pip requirements.

        **default options** ::
            virtualenvdir={{ deploy_dir }}/.virtualenv
            pip_projectfile={{ deploy_dir }}/source/requirements.txt


        #. **INSTALL**

           Install virtualenv in it not exists.
           Create virtual env and update pip requirements

        #. **UPDATE**

           Update pip requirements if it needed


    cron
        Add project cron tasks in crond. `cron source`_ 

        .. note ::
           Default <cron_projectfile> is crontab in project root. File in cron format.
           Commands from this file will be runned from <site_user> relative project root
           and with enabled project virtualenv

        **default options** ::

            cron_projectfile={{ project_sourcedir }}/crontab
            cron_outputfile=/etc/cron.d/{{ project }}-{{ branch }}


        #. **INSTALL**, **UPDATE**

           Parse project crontab file and add it to cron.

        #. **REMOVE**

           Remove project cron tasks from cron.


    nginx
        nginx_ support

        **default options** ::

            nginx_target_confpath=/etc/nginx/sites-enabled/{{ project }}.{{ branch }}.conf
            nginx_source_confpath=<deploy_dir>/deploy/nginx.conf

        #. **INSTALL**

           Install nginx if not exist
           Create link <nginx_confpath> to deploy nginx.conf ( its make other templates ex django or tornado )
           Restart nginx

        #. **REMOVE**

           Remove link <nginx_confpath>
           Restart nginx


    supervisor
        supervisor_ support.

        **default options** ::
            supervisor_target_confpath=/etc/supervisor/conf.d/{{ project }}.{{ branch }}.conf
            supervisor_source_confpath=<deploy_dir>/deploy/supervisor.conf
            supervisor_taskname=<project>.<branch>


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
        uwsgi_ support. Contains nginx and supervisor configs. `uwsgi source`_

        .. note ::
           uwsgi template waiting file ``wsgi.py`` in project source root with defined wsgi application

        **default options** ::
            uwsgi_source_confpath=<deploy_dir>/deploy/uwsgi.xml


    zeta
        zeta_ support. Packing project static files. `zeta source`_

        #. **INSTALL**, **UPDATE**

           Packing js, css, scss files from deploy static dir.


    compass
        compass_ support. `compass source`_

    html
        static html site. Contains nginx config. Serve files from project staticdir.


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

.. _nginx: http://www.nginx.org/
.. _supervisor: http://supervisord.org/
.. _git: http://git-scm.com/
.. _uwsgi: http://projects.unbit.it/uwsgi/
.. _zeta: https://github.com/klen/zeta-library
.. _compass: http://compass-style.org/
