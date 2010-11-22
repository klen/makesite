CRON_CRONFILE={{ cron_conffile }}

if [ -f $CRON_CRONFILE ]; then
    echo "  * Remove cron file '$CRON_CRONFILE'."
    sudo rm -rf $CRON_CRONFILE
fi
