BRANCH={{ branch }}
PROJECT={{ project }}
NGINX_CONF_PATH={{ nginx_conf_path }}
SUPERVISOR_CONF_PATH={{ supervisor_conf_path }}

NGINX_CONF=$NGINX_CONF_PATH/$BRANCH.$PROJECT.conf
SUPERVISOR_CONF=$SUPERVISOR_CONF_PATH/$BRANCH.$PROJECT.conf

echo '  * Remove link to nginx conf:'$NGINX_CONF
sudo rm -rf $NGINX_CONF

echo '  * Remove link to supervisor conf:'$SUPERVISOR_CONF
sudo rm -rf $SUPERVISOR_CONF
