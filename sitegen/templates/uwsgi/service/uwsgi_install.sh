BRANCH={{ branch }}
PROJECT={{ project }}
DEPLOY_DIR={{ deploy_dir }}
NGINX_CONF_PATH={{ nginx_conf_path }}
SUPERVISOR_CONF_PATH={{ supervisor_conf_path }}

NGINX_CONF=$NGINX_CONF_PATH/$BRANCH.$PROJECT.conf
SUPERVISOR_CONF=$SUPERVISOR_CONF_PATH/$BRANCH.$PROJECT.conf
VIRTUALENV=$DEPLOY_DIR/.virtualenv

echo '  * Create virtualenv:'$VIRTUALENV
sudo virtualenv --no-site-packages $VIRTUALENV

echo '  * Create link to nginx conf:'$NGINX_CONF
sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONF  

echo '  * Create link to supervisor conf:'$SUPERVISOR_CONF
sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONF 
