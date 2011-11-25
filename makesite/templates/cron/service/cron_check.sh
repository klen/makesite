#!/bin/bash

. $(dirname $0)/utils.sh

# Check cron installed.
check_program cron "Install cron package"
