#!/bin/bash

source $(dirname $0)/utils.sh | exit 1

# Check supervisor installed
check_program supervisord "Install supervisor package"
check_program supervisorctl "Install supervisor package"
