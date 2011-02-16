Usage
=====


Install
-------

**Makesite** should be installed using pip_ or easy_install: ::

    pip install makesite

    easy_install makesite


Setup
-----

The variable SITES_HOME tell makesite where to place your sites.
Add this lines to your shell startup file .bashrc, .profile, etc) ::

    if [ -f /usr/local/bin/makesitewrapper.sh ]; then
        export SITES_HOME=PATH_TO_YOUR_SITES_HOME
        source /usr/local/bin/makesitewrapper.sh
    fi

Also it add you more makesite comands: cdsite, envsite, worksite, lssites and autocomplete in bash


Help
----

Run makesite for help message. ::

    $ makesite
    Usage: makesite -p PATH PROJECTNAME [-b BRANCH] [-t TEMPLATE] [-c CONFIG] [-s SOURCE_PATH] [-m MODULENAME or MODULEPATH] [-i]

    'Makesite' is scripts collection for create base project dirs and config
    files.   See also next utilities: installsite, updatesite, removesite, cdsite,
    worksite, lssites, statsites.

    Options:
    --version             show program's version number and exit
    -h, --help            show this help message and exit
    -i, --info            Show compiled project params and exit.
    -p PATH, --path=PATH  Path to base deploy projects dir. Required if not set
                            SITES_HOME environment.
    -b BRANCH, --branch=BRANCH
                            Project branch.
    -t TEMPLATE, --template=TEMPLATE
                            Config templates.
    -c CONFIG, --config=CONFIG
                            Config file.
    -m MODULE, --module=MODULE
                            Deploy module
    -s SRC, --src=SRC     Path to source (filesystem or repository address ex:
                            git+http://git_adress, /test/myproject).


Commands
--------

* **makesite** - base makesite command used for deploy projects

* **installsite** - command run install scripts from deployed project, makesite auto run this command in deploy
  Can be used for repeat install if it break in deploy.

* **updatesite** - command run update scripts from deployed project in templates order. 
  Used for update projects.

* **removeproject** - command run removed scripts from deployed project in templates order.
  Used for remove project.

* **lssites** - show list deployed projects

* **cdsite** - change directory to projects dir
  Used for quick change directory because working bash autocomplete on deployed projects

* **siteinfo** - show site deploy config information

* **envsite** - activate project virtualenv

* **worksite** - cdsite and envsite in one command. Change dir to project dir and activate virtualenv


.. _pip: http://pip.openplans.org/
