CRON_CRONFILE={{ cron_conffile }}
CRON_PROJECTFILE={{ cron_projectfile }}
CRON_PARSESCRIPT={{ deploy_dir }}/service/cron_parse.py

if ! which cron >/dev/null; then echo "  * I require cron but it's not installed."; exit 0; fi

if [ -f $CRON_PROJECTFILE ]; then
    sudo python $CRON_PARSESCRIPT
    # echo '  * Create link to project crontabfile:'$CRON_PROJECTFILE
    # sudo ln -sf $CRON_PROJECTFILE $CRON_CRONFILE
fi
