#!/bin/sh

# Variables
PROGRAMM_NAME={{ project }}.{{ branch }}.celeryd
DEPLOY_DIR={{ deploy_dir }}
SUPERVISOR_CELERY_CONFPATH={{ supervisor_celery_confpath }}

# Check supervisor installed
which supervisord 1>/dev/null || {
        echo "  * SUPERVISOR not found! Attempting to install..."
        if [ -f /etc/lsb-release ] ; then
                sudo apt-get install supervisor -y
        elif [ -f /etc/fedora-release ] ; then
                sudo yum install supervisor
        elif [ -f /etc/debian_version ] ; then
                sudo apt-get install supervisor
        fi
}

echo '  * Create link to supervisor conf:'$SUPERVISOR_CELERY_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/supervisor.celeryd.conf $SUPERVISOR_CELERY_CONFPATH

if [ -f /etc/init.d/supervisor ]; then
    echo '  * Update supervisord for celeryd'
    sudo supervisorctl reread
    sudo supervisorctl reload $PROGRAMM_NAME
fi
