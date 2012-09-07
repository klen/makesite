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

.. envvar:: MAKESITE_HOME

The variable :envvar:`MAKESITE_HOME` tell makesite where to place your sites.

Run ``makesite shell`` for generate shell configuration.

.. code-block:: bash

    $ makesite shell -p <path_to_deploy_dir> >> ~/.bashrc

Also it adds to you more makesite commands_ and autocomplete in bash

You may want to create base config file ``makesite.ini`` in :envvar:`MAKESITE_HOME`, with your project settings:
ex.: ``/sites/makesite.ini``:

.. code-block:: ini

   [Main]
   domain=%(branch)s.%(project)s.dev.me
   src=git+gitolite@git.dev.intaxi:%(project)s.git
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
      usage: makesite [-h] [-v]
                      {info,shell,install,update,module,ls,template,uninstall}

      Base dispather

      positional arguments:
      {info,shell,install,update,module,ls,template,uninstall}
                              Choose action: info, shell, install, update, module,
                              ls, template, uninstall

      optional arguments:
      -h, --help            show this help message and exit
      -v, --version         Show makesite version

Run ``makesite subcommand --help`` for subcommand help message. ::

    $ makesite install --help
    usage: makesite install [-h] [-v] [-p PATH] [-b BRANCH] [-m MODULE] [-r] [-i]
                            [-s SRC] [-t TEMPLATE] [-c CONFIG]
                            PROJECT

    Install site from sources or module

    positional arguments:
    PROJECT               Project name

    optional arguments:
    -h, --help            show this help message and exit
    -v, --version         Show makesite version
    -p PATH, --path PATH  Path to makesite sites instalation dir. You can set it
                            in $MAKESITE_HOME env variable.
    -b BRANCH, --branch BRANCH
                            Name of branch.
    -m MODULE, --module MODULE
                            Name of module. Install module.
    -r, --repeat          Repeat installation.
    -i, --info            Show project install options and exit.
    -s SRC, --src SRC     Source path for installation.
    -t TEMPLATE, --template TEMPLATE
                            Force templates.
    -c CONFIG, --config CONFIG
                            Config file.


Commands
--------

.. data:: install

    Copy project from source (filepath, git, hg, svn), deploy templates and run install
    scripts. ::

        makesite install PROJECT [OPTIONS]

.. autofunction:: makesite.main.update

.. data:: uninstall

   Run removed scripts from deployed project in templates order.
   Used for remove project. ::

        $ makesite uninstall PROJECT_PATH 

.. autofunction:: makesite.main.ls

.. data:: info

   Show site deploy config information


.. _pip: http://pip.openplans.org/
.. _setuptools: http://pypi.python.org/pypi/setuptools 
