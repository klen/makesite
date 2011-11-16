.. highlight:: bash

Examples
========

    .. note ::

        In this examples user have :envvar:`MAKESITE_HOME` = ``/sites``


Deploy standart django module to project **beta**: ::
    
    makesite install beta -m django 

Create tornado project sceleton, with auto create project postgres user and db: ::

    makesite install tornado-project -t db-postgres,tornado 

Deploy branch **test** from project **alpha**.
Git source path for project defined in the config file: ``/sites/makesite.ini`` ::

    makesite install alpha -b test

Append template zeta to existed project alpha::

    makesite template add zeta /sites/alpha/beta

Deploy branch **master** from project **dummy** from source ``git@test.dev/test.git``: ::

    makesite install dummy -s git+git@test.dev/test.git

Update branch **test** from project **alpha**: ::

    makesite update /sites/alpha/test

Remove site **remove_me**: ::

    makesite uninstall /sites/remove_me/master

View deployed projects: ::

    makesite ls

View all deployed project **alpha** settings: ::

    makesite info /sites/alpha/master

Goto to project source dir and activate project virtualenv: ::

    worksite /sites/alpha/master
