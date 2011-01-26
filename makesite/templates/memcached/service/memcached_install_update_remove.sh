#!/bin/sh

MEMCACHED_HOST={{ memcached_host }}
MEMCACHED_PORT={{ memcached_port }}

if [ -z "$MEMCACHED_HOST" ] || [ -z "$MEMCACHED_PORT" ]; then
    exit 0
fi

python -c "import memcache" 2>/dev/null || {
    echo "  * Python memcache not found! Attempting to install..."
    sudo pip install python-memcached
}

echo "  * Flush memcahed '$MEMCACHED_HOST:$MEMCACHED_PORT'"
python -c "import memcache; memcache.Client(['$MEMCACHED_HOST:$MEMCACHED_PORT']).flush_all()"
