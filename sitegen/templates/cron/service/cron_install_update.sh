CRON_CRONFILE={{ cron_conffile }}
CRON_PROJECTFILE={{ cron_projectfile }}
CRON_PARSESCRIPT={{ deploy_dir }}/service/cron_parse.py
CRON_GENERATEFILE={{ deploy_dir }}/deploy/{{ project }}.{{ branch }}.cron

if ! which cron >/dev/null; then echo "  * I require cron but it's not installed."; exit 0; fi

if [ -f $CRON_PROJECTFILE ]; then
    sudo python $CRON_PARSESCRIPT
    if [ -f $CRON_GENERATEFILE ]; then
        echo '  * Create link to generate project crontabfile:'$CRON_GENERATEFILE
        sudo ln -sf $CRON_GENERATEFILE $CRON_CRONFILE
    fi
fi
