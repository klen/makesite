#!/bin/sh

# Variables
MEMCACHED_HOST={{ memcached_host }}
MEMCACHED_PORT={{ memcached_port }}

if [ -z "$MEMCACHED_HOST" ] || [ -z "$MEMCACHED_PORT" ]; then
    # pass
    exit 0
fi

# Install memcached on localhost
if [ $MEMCACHED_HOST = 'localhost' ]; then
    which memcached 1>/dev/null || {
            echo "  * Memcache not found! Attempting to install..."
            # Ubuntu
            if [ -f /etc/lsb-release ] ; then
                sudo apt-get install memcached -y

            # Debian
            elif [ -f /etc/debian_version ] ; then
                sudo apt-get install memcached

            # Fedora
            elif [ -f /etc/fedora-release ] ; then
                sudo yum install memcached
            fi
    }
fi

python -c "import memcache" 2>/dev/null || {
    echo "  * Python memcache not found! Attempting to install..."
    sudo pip install python-memcached
}

echo "  * Flush memcahed '$MEMCACHED_HOST:$MEMCACHED_PORT'"
python -c "import memcache; memcache.Client(['$MEMCACHED_HOST:$MEMCACHED_PORT']).flush_all()"
