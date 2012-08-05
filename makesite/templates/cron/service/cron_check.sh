#!/bin/bash

source $(dirname $0)/utils.sh | exit 1

# Check cron installed.
check_program cron "Install cron package"
