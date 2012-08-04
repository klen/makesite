#!/bin/bash

source $(dirname $0)/utils.sh

# Check supervisor installed
check_program supervisord "Install supervisor package"
check_program supervisorctl "Install supervisor package"
