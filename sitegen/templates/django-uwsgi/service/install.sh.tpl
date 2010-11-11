NGINX_CONF=%(nginx_conf_path)s/%(branch)s.%(project_name)s.conf
SUPERVISOR_CONF=%(supervisor_conf_path)s/%(branch)s.%(project_name)s.conf

echo '  * Create link to nginx conf:'$NGINX_CONF
ln -sf %(deploy_dir)s/deploy/nginx.conf $NGINX_CONF  

echo '  * Create link to supervisor conf:'$SUPERVISOR_CONF
ln -sf %(deploy_dir)s/deploy/supervisor.conf $SUPERVISOR_CONF 
