#!/bin/bash

. $(dirname $0)/utils.sh

# Check supervisor installed
check_program supervisord
check_program supervisorctl
