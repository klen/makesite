DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}
VIRTUALENVDIR={{ virtualenvdir }}

_require () {
    echo "  * I require $1 but it's not installed."
}

if which virtualenv >/dev/null; then
    echo '  * Create virtualenv:'$VIRTUALENVDIR
    sudo virtualenv --no-site-packages $VIRTUALENVDIR
else
    _require virtualenv 
fi

if which nginx >/dev/null; then
    echo '  * Create link to nginx conf:'$NGINX_CONFPATH
    sudo ln -sf $DEPLOY_DIR/deploy/nginx.conf $NGINX_CONFPATH
else
    _require nginx 
fi

if which supervisord >/dev/null; then
    echo '  * Create link to supervisor conf:'$SUPERVISOR_CONF
    sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONF 
else
    _require supervisor 
fi
