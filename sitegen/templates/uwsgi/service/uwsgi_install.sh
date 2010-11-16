DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}
VIRTUALENVDIR={{ virtualenvdir }}

_create_virtualenv () {
    # Check virtualenv
    type -P virtualenv &>/dev/null || { echo "I require virtualenv but it's not installed.  Aborting." >&2; return 1; }

    echo '  * Create virtualenv:'$VIRTUALENVDIR
    sudo virtualenv --no-site-packages $VIRTUALENVDIR
}

_link_to_nginx () {
    # Check nginx
    type -P nginx &>/dev/null || { echo "I require nginx but it's not installed.  Aborting." >&2; return 1; }
    
    echo '  * Create link to nginx conf:'$NGINX_CONFPATH
    sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONFPATH
}

_link_to_supervisor () {
    # Check supervisord
    type -P supervisord &>/dev/null || { echo "I require supervisord but it's not installed.  Aborting." >&2; return 1; }
    
    echo '  * Create link to supervisor conf:'$SUPERVISOR_CONF
    sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONF 
}

_create_virtualenv
_link_to_nginx
_link_to_supervisor
