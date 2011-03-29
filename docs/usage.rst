Usage
=====


Install
-------

:data:`makesite` should be installed using pip_ or setuptools_:

.. code-block:: bash

    pip install makesite

    easy_install makesite


Setup
-----

.. envvar:: SITES_HOME

The variable :envvar:`SITES_HOME` tell makesite where to place your sites.
Add this lines to your shell startup file ``.bashrc``, ``.profile``, etc)

.. code-block:: bash

    if [ -f /usr/local/bin/makesitewrapper.sh ]; then
        export SITES_HOME=<PATH_TO_YOUR_SITES_HOME>
        source /usr/local/bin/makesitewrapper.sh
    fi

Also it adds to you more makesite commands_ and autocomplete in bash

You may want to create base config file ``makesite.ini`` in :envvar:`SITES_HOME`, with your project settings:
ex.: ``/sites/makesite.ini``:

.. code-block:: ini

   [Main]
   domain={{ branch + '.' if not branch == 'master' else ''}}{{ project }}.klen.xxx
   src=git+gitolite@git.dev.server:{{ project }}.git
   pguser=postgres
   pghost=pg.dev.server
   ; password for create db and users for projects
   pgpassword=blablabla
   memcached_host=localhost
   ; server mode, example for switch django settings
   mode=dev

This will allow you to identify any :doc:`common settings <configuration>` for projects.


Help
----

.. data:: makesite

    Base command used for deploy projects.

Run ``makesite --help`` for help message. ::

    $ makesite --help
    usage: makesite [-h] [-i] [-b BRANCH] [-t TEMPLATE] [-a] [-c CONFIG]
                    [-m MODULE] [-s SRC] [-v]
                    project

    'Makesite' is scripts collection for create base project dirs and config
    files.

    positional arguments:
    project               Project name

    optional arguments:
    -h, --help            show this help message and exit
    -i, --info            Show compiled project params and exit.
    -b BRANCH, --branch BRANCH
                            Project branch.
    -t TEMPLATE, --template TEMPLATE
                            Config templates.
    -a, --append          Append template to exists project.
    -c CONFIG, --config CONFIG
                            Config file.
    -m MODULE, --module MODULE
                            Deploy module
    -s SRC, --src SRC     Path to source (filesystem or repository address ex:
                            git+http://git_adress).
    -v, --version         Show makesite version

    See also next utilities: installsite, updatesite, removesite, cdsite,
    worksite, lssites, statsites.


Commands
--------

.. data:: installsite

   Run install scripts from deployed project, makesite auto run this command in deploy.
   Can be used for repeat install if it break in deploy. ::

        $ installsite 
        Usage: installsite PROJECT_BRANCH_PATH
        'installsite' part of makesite scripts.
        Activate install hooks for target project. Run tests for master branch wich option --autotest.


.. data:: updatesite

   Run update scripts from deployed project in templates order. 
   Used for update projects. ::

        $ updatesite 
        Usage: updatesite PROJECT_BRANCH_PATH
        'updatesite' part of makesite scripts.
        Activate update hooks for target project. Run tests for master branch wich option --autotest.

.. data:: removesite

   Run removed scripts from deployed project in templates order.
   Used for remove project. ::

        $ removesite 
        Usage: removesite PROJECT_BRANCH_PATH
        'removesite' part of makesite scripts. Activate remove hooks for target project and remove project dir.

.. data:: lssites

   Show list deployed projects.

.. data:: cdsite

   Change directory to projects dir.
   Used for quick change directory because working bash autocomplete on deployed projects

.. data:: siteinfo

   Show site deploy config information

.. data:: envsite

   Activate project virtualenv

.. data:: worksite

   :data:`cdsite` and :data:`envsite` in one command. Change dir to project dir and activate virtualenv


.. _pip: http://pip.openplans.org/
.. _setuptools: http://pypi.python.org/pypi/setuptools 
