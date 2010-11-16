CRON_CRONFILE={{ cron_conf_file }}
CRON_PROJECTFILE={{ cron_project_file }}

# Check cron
type -P cron &>/dev/null || { echo "I require cron but it's not installed.  Aborting." >&2; exit 1; }

sudo rm -rf $CRON_CRONFILE
