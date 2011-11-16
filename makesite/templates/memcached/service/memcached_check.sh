#!/bin/bash

. $(dirname $0)/utils.sh

MEMCACHED_HOST={{ memcached_host }}

# Check memcached on localhost
if [[ "$MEMCACHED_HOST" == "localhost" || "$MEMCACHED_HOST" == "127.0.0.1" ]]; then
    check_program memcached
fi

# Check netcat
check_program netcat
