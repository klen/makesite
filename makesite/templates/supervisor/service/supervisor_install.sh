#!/bin/sh

# Variables
DEPLOY_DIR={{ deploy_dir }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}
PROGRAMM_NAME={{ project }}.{{ branch }}

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
echo '  * Create link to supervisor conf:'$SUPERVISOR_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONFPATH

# Restart supervisor
if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord'
    sudo supervisorctl reread
    sudo supervisorctl reload $PROGRAMM_NAME
fi
