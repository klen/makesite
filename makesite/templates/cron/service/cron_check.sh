#!/bin/bash

source {{ project_servicedir }}/.bsfl

# Check cron installed.
check_program cron
