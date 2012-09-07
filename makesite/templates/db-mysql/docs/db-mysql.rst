DB-Mysql
-----------

**db-mysql** — Create project role and database in mysql if it not exists.


Requirements
^^^^^^^^^^^^
Installed mysql


Variables
^^^^^^^^^

.. option:: mysqluser

    MySQL user has rights for create DB

    Default: root

.. option:: mysqlpassword

    Password for { mysqluser }

    Default: root

.. option:: mysqlhost

    Host of mysql DB

    Default: localhost

.. option:: mysqlport

    Port of mysql DB

    Default: 3306

.. option:: dbname

    Name of project database

    Default: { project }_master

.. option:: dbuser

    Owner name of project database

    Default: { project }

.. option:: dbpassword

    Password for { db_user }

    Default: { project }


Install operation
^^^^^^^^^^^^^^^^^

Create role { dbuser } and database { dbname } if it not exists.

