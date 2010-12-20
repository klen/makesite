..   -*- mode: rst -*-

sitegen
#######

Sitegen is collection scripts for make and control site structure.

.. contents::

Requirements
-------------

- python >= 2.5
- pip >= 0.8


Installation
------------

**Sitegen** should be installed using pip: ::

    pip install sitegen


Setup
------

The variable SITES_HOME tell sitegen where to place your sites.
Add this lines to your shell startup file .bashrc, .profile, etc) ::

    if [ -f /usr/local/bin/sitegenwrapper.sh ]; then
        export SITES_HOME=PATH_TO_YOUR_SITES_HOME
        source /usr/local/bin/sitegenwrapper.sh
    fi


Using
-----
Run sitegen for help message.

