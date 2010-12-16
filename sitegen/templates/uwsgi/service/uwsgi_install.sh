DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

which nginx 1>/dev/null || {
        echo "  * NGINX not found! Attempting to install..."
        if [ -f /etc/lsb-release ] ; then
                sudo apt-get install nginx
        elif [ -f /etc/fedora-release ] ; then
                sudo yum install nginx
        elif [ -f /etc/debian_version ] ; then
                sudo apt-get install nginx
        fi
}
echo '  * Create link to nginx conf:'$NGINX_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONFPATH

which supervisord 1>/dev/null || {
        echo "  * SUPERVISOR not found! Attempting to install..."
        if [ -f /etc/lsb-release ] ; then
                sudo apt-get install supervisor
        elif [ -f /etc/fedora-release ] ; then
                sudo yum install supervisor
        elif [ -f /etc/debian_version ] ; then
                sudo apt-get install supervisor
        fi
}
echo '  * Create link to supervisor conf:'$SUPERVISOR_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONFPATH
