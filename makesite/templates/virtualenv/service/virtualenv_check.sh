#!/bin/bash

. $(dirname $0)/utils.sh

# Check pip and virtualenv
check_program pip "Install python-pip package"
check_program virtualenv "Install python-virtualenv package"
