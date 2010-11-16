CRON_FILE={{ deploy_dir }}/source/crontab
CRON_CONF_FILE=/etc/cron.d/{{ branch }}.{{ project }}.cron

sudo rm -rf $CRON_CONF_FILE
