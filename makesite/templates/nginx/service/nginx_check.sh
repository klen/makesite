#!/bin/bash

. $(dirname $0)/utils.sh

# Check nginx
check_program nginx "Install nginx package"
