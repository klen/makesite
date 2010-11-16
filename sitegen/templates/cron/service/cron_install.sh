CRON_FILE={{ deploy_dir }}/source/crontab
CRON_CONF_FILE=/etc/cron.d/{{ branch }}.{{ project }}.cron

if [ -f $CRON_FILE ]; then
    echo '  * Create link to project crontabfile:'$CRON_FILE
    sudo ln -sf $CRON_FILE $CRON_CONF_FILE
fi
