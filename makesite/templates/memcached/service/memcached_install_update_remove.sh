#!/bin/bash

# Import BSFL
PROJECT_SERVICEDIR={{ project_servicedir }}
source $PROJECT_SERVICEDIR/.bsfl

# Variables
MEMCACHED_HOST={{ memcached_host }}
MEMCACHED_PORT={{ memcached_port }}

if [ -z "$MEMCACHED_HOST" ] || [ -z "$MEMCACHED_PORT" ]; then
    msg_warning "Memcached host and port not defined"
    exit 0
fi

msg_info "Flush memcahed $MEMCACHED_HOST:$MEMCACHED_PORT"
python -c "import memcache; memcache.Client(['$MEMCACHED_HOST:$MEMCACHED_PORT']).flush_all()"
