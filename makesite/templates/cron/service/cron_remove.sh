#!/bin/sh

# Variables
CRON_OUTPUTFILE={{ cron_outputfile }}

if [ -f $CRON_OUTPUTFILE ]; then
    echo "  * Remove cron file '$CRON_OUTPUTFILE'."
    sudo rm -rf $CRON_OUTPUTFILE
fi
