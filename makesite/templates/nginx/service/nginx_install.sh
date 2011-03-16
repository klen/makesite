#!/bin/sh

# Variables
DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}

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
echo '  * Create link to nginx conf:'$NGINX_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONFPATH

# Restart nginx
if [ -f /etc/init.d/nginx ]; then
    echo '  * Restart nginx'
    if [ ! -z "`pgrep nginx`" ]; then
        sudo /etc/init.d/nginx stop
    fi
    sudo /etc/init.d/nginx start
fi
