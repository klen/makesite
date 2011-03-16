#!/bin/sh

# Variables
CRON_PROJECTFILE={{ cron_projectfile }}
CRON_PARSESCRIPT={{ deploy_dir }}/service/cron_parse.py


# Check cron installed.
sudo which cron 1>/dev/null || {
    echo "  * Cron not found! Attempting to install..."
    if [ -f /etc/lsb-release ] ; then
        sudo apt-get install cron -y
    elif [ -f /etc/fedora-release ] ; then
        sudo yum install cron
    elif [ -f /etc/debian_version ] ; then
        sudo apt-get install cron
    fi
}

if [ -f $CRON_PROJECTFILE ]; then
    sudo python $CRON_PARSESCRIPT
fi
