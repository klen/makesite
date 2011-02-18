#!/bin/sh

# Check uwsgi and install if not exist
which uwsgi 1>/dev/null || {
    if [ -f /etc/lsb-release ] ; then
        sudo apt-get install python-setuptools -y
    elif [ -f /etc/fedora-release ] ; then
        sudo yum install python-setuptools
    elif [ -f /etc/debian_version ] ; then
        sudo apt-get install python-setuptools -y
    fi
    sudo pip install http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
    sudo /etc/init.d/supervisor stop
    sudo /etc/init.d/supervisor start
}
