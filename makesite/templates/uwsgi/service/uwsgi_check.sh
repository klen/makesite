#!/bin/bash

. $(dirname $0)/utils.sh

# Check uwsgi
check_program uwsgi "Install uwsgi and uwsgi-plugins-all packages"
