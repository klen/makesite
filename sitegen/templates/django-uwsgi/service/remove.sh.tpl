NGINX_CONF=%(nginx_conf_path)s/%(branch)s.%(project_name)s.conf
SUPERVISOR_CONF=%(supervisor_conf_path)s/%(branch)s.%(project_name)s.conf

echo '  * Remove link to nginx conf:'$NGINX_CONF
rm -rf $NGINX_CONF

echo '  * Remove link to supervisor conf:'$SUPERVISOR_CONF
rm -rf $SUPERVISOR_CONF
