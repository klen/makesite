DB-Postgres
-----------

**db-postgres** — Create project role and database in postgres if it not exists.


Requirements
^^^^^^^^^^^^
Installed `psql <http://www.postgresql.org/docs/8.2/static/app-psql.html>`_ client.


Variables
^^^^^^^^^

.. option:: pguser

    PG user has rights for create DB

    Default: postgres

.. option:: pgpassword

    Password for { pguser }

    Default: postgres

.. option:: pghost

    Host of postgres DB

    Default: localhost

.. option:: pgport

    Port of postgres DB

    Default: 5432

.. option:: dbname

    Name of project database

    Default: { project }_master

.. option:: dbuser

    Owner name of project database

    Default: { project }

.. option:: dbpassword

    Password for { dbuser }

    Default: { project }


Install operation
^^^^^^^^^^^^^^^^^

Create role { dbuser } and database { dbname } if it not exists.
