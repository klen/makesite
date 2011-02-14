..   -*- mode: rst -*-

Makesite
########

Makesite is collection scripts for make and control site structure.

.. contents::

Requirements
-------------

- python >= 2.5
- pip >= 0.8


Installation
------------

**Makesite** should be installed using pip: ::

    pip install makesite


Setup
------

The variable SITES_HOME tell makesite where to place your sites.
Add this lines to your shell startup file .bashrc, .profile, etc) ::

    if [ -f /usr/local/bin/makesitewrapper.sh ]; then
        export SITES_HOME=PATH_TO_YOUR_SITES_HOME
        source /usr/local/bin/makesitewrapper.sh
    fi


Using
-----
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
                            git+http://git_adress).


Examples
--------

Deploy standart django template from makesite to project "beta": ::
    
    makesite -m django beta


Deploy branch 'test' from project 'alpha': ::

    makesite -b test alpha

Deploy branch 'master' from project 'alpha' from source git@test.dev/test.git: ::

    makesite alpha -s git+git@test.dev/test.git

Update branch 'test' from project 'alpha': ::

    updatesite /sites/alpha/test

View deployed projects: ::

    lssites
    statsites

And etc, etc, etc
