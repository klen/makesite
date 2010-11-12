NGINX_CONF={{nginx_conf_path}}/{{branch}}.{{project_name}}.conf
SUPERVISOR_CONF={{supervisor_conf_path}}/{{branch}}.{{project_name}}.conf
VIRTUALENV={{deploy_dir}}/.virtualenv

echo '  * Create virtualenv:'$VIRTUALENV
virtualenv --no-site-packages $VIRTUALENV

echo '  * Create link to nginx conf:'$NGINX_CONF
ln -sf {{deploy_dir}}/deploy/nginx.conf $NGINX_CONF  

echo '  * Create link to supervisor conf:'$SUPERVISOR_CONF
ln -sf {{deploy_dir}}/deploy/supervisor.conf $SUPERVISOR_CONF 
