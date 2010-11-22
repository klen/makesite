..   -*- mode: rst -*-

#######
sitegen
#######

Simple script for make site structure.

Installation
------------

Sitegen should be installed using pip:

    **pip install git+git://github.com/klen/sitegen.git**

The variable SITES_HOME tell sitegen where to place your sites.
Add this lines to your shell startup file .bashrc, .profile, etc)

::

    if [ -f /usr/local/bin/sitegenwrapper.sh ]; then
        export SITES_HOME=PATH_TO_YOUR_SITES_HOME
        source /usr/local/bin/sitegenwrapper.sh
    fi

