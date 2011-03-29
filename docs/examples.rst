.. highlight:: bash

Examples
========

    .. note ::

        In this examples user have :envvar:`SITES_HOME` = ``/sites``


Deploy standart django template from makesite to project **beta**: ::
    
    makesite -m django beta

Create tornado project sceleton, with auto create project postgres user and db: ::

    makesite -t db-postgres,tornado tornado-project

Deploy branch **test** from project **alpha**.
Git source path for project defined in the config file: ``/sites/makesite.ini`` ::

    makesite -b test alpha

Append template zeta to existed project alpha::

    makesite alpha -a -t test

Deploy branch **master** from project **dummy** from source ``git@test.dev/test.git``: ::

    makesite dummy -s git+git@test.dev/test.git

Update branch **test** from project **alpha**: ::

    updatesite /sites/alpha/test

Remove site **remove_me**: ::

    removesite /sites/remove_me/master

View deployed projects: ::

    lssites
    statsites

View all deployed project **alpha** settings: ::

    siteinfo /sites/alpha/master

Goto to project source dir and activate project virtualenv: ::

    worksite /sites/alpha/master
