CRON_CRONFILE={{ cron_conf_file }}
CRON_PROJECTFILE={{ cron_project_file }}

# Check cron
type -P cron &>/dev/null || { echo "I require cron but it's not installed.  Aborting." >&2; exit 1; }

if [ -f $CRON_PROJECTFILE ]; then
    echo '  * Create link to project crontabfile:'$CRON_PROJECTFILE
    sudo ln -sf $CRON_PROJECTFILE $CRON_CRONFILE
fi
