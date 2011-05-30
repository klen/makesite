#!/bin/sh

# Variables
NGINX_SOURCE_CONFPATH={{ nginx_source_confpath }}
NGINX_TARGET_CONFPATH={{ nginx_target_confpath }}

# Check nginx and install if not exist
sudo which nginx 1>/dev/null || {
        echo "  * NGINX not found! Attempting to install..."

        # Ubuntu
        if [ -f /etc/lsb-release ] ; then
            sudo add-apt-repository ppa:nginx/stable
            sudo apt-get update
            sudo apt-get install nginx-full -y

        # Debian
        elif [ -f /etc/debian_version ] ; then
            sudo apt-get install nginx -y

        # Fedora
        elif [ -f /etc/fedora-release ] ; then
            sudo yum install nginx
        fi
}

# Add site to nginx enabled sites
echo '  * Create link to nginx conf:'$NGINX_TARGET_CONFPATH
sudo ln -sf $NGINX_SOURCE_CONFPATH $NGINX_TARGET_CONFPATH

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    if [ ! -z "`pgrep nginx`" ]; then
        echo '  * Stop nginx'
        sudo /etc/init.d/nginx stop
    fi
    echo '  * Start nginx'
    sudo /etc/init.d/nginx start
fi
