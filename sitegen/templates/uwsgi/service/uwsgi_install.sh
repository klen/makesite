DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}

which nginx 1>/dev/null || { echo "ERROR: * I require nginx but it's not installed."; exit 0; }
echo '  * Create link to nginx conf:'$NGINX_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONFPATH

which supervisord 1>/dev/null || { echo "ERROR: * I require supervisord but it's not installed."; exit 0; }
echo '  * Create link to supervisor conf:'$SUPERVISOR_CONFPATH
sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONFPATH
