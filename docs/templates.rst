Standart templates
==================

.. contents::

src-dir
-------

`src-dir-link`_

    .. note ::

        Template automatic added to project if project source is local dir

1. **UPDATE**

   Copy project source from source dir to deploy source dir

   Copy static dir from deploy source static dir to deploy static dir


src-git
-------

`src-git-link`_

    .. note ::

        Template automatic added to project if project source is git repository

1. **UPDATE**

   Update git project source dir



db-postgres
-----------

db-postgres-link_

    .. note ::

        Require <pguser>, <pghost>, <pgpassword> variables in configs with admin rights

1. **INSTALL**

    Create postgres user <dbuser> if not exists, default is <project> with password <dbpassword> default is <project>

    Create postgres db <dbname> default <project>_master


memcached
---------

memcached-link_

    .. note ::

        Default memcached_host=localhost, memcached_port=11211

2. **INSTALL**, **UPDATE**

    Install python-memcached if not exist and flush memcached cache


nginx
-----

nginx-link_

    .. note ::

        Default nginx configs path <nginx_confpath>: /etc/nginx/sites-enabled/{{ project }}.{{ branch }}.conf 

1. **INSTALL**

   Install nginx if not exist

   Create link <nginx_confpath> to deploy nginx.conf ( its make other templates ex django or tornado )

   Restart nginx

2. **REMOVE**

   Remove link <nginx_confpath>

   Restart nginx


supervisor
----------

supervisor-link_

    .. note ::

        Default supervisor configs path <supervisor_confpath>: /etc/supervisor/conf.d/{{ project }}.{{ branch }}.conf

1. **INSTALL**

    Install supervisor if not exists

    Create link to <supervisor_confpath> its make another templates ex: django, tornado

    Reread supervisor configs

2. **UPDATE**

   Restart supervisor project task

3. **REMOVE**

    Remove link <supervisor_confpath>

    Reread supervisor configs




.. _src-dir-link: https://github.com/klen/makesite/tree/master/makesite/templates/src-dir/service
.. _src-git-link: https://github.com/klen/makesite/tree/master/makesite/templates/src-git/service
.. _db-postgres-link: https://github.com/klen/makesite/tree/master/makesite/templates/db-postgres/service
.. _memcached-link: https://github.com/klen/makesite/tree/master/makesite/templates/memcached/service
.. _nginx-link: https://github.com/klen/makesite/tree/master/makesite/templates/nginx/service
.. _supervisor-link: https://github.com/klen/makesite/tree/master/makesite/templates/supervisor/service
