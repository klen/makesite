#!/bin/sh

# Variables
SUPERVISOR_TARGET_CONFPATH={{ supervisor_target_confpath }}
SUPERVISOR_SOURCE_CONFPATH={{ supervisor_source_confpath }}
SUPERVISOR_TASKNAME={{ supervisor_taskname }}

# Check supervisor and install if not exist
which supervisord 1>/dev/null || {
        echo "  * SUPERVISOR not found! Attempting to install..."
        if [ -f /etc/lsb-release ] ; then
                sudo apt-get install supervisor -y
        elif [ -f /etc/fedora-release ] ; then
                sudo yum install supervisor
        elif [ -f /etc/debian_version ] ; then
                sudo apt-get install supervisor -y
        fi
}                                    

# Add project config to supervisor
echo '  * Create link to supervisor conf:'$SUPERVISOR_TARGET_CONFPATH
sudo ln -sf $SUPERVISOR_SOURCE_CONFPATH $SUPERVISOR_TARGET_CONFPATH

# Restart supervisor
if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord'
    sudo supervisorctl reread
    sudo supervisorctl reload
fi
