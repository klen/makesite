DEPLOY_DIR={{ deploy_dir }}
NGINX_CONFPATH={{ nginx_confpath }}
SUPERVISOR_CONFPATH={{ supervisor_confpath }}
VIRTUALENVDIR={{ virtualenvdir }}

_require () {
    echo "  * I require $1 but it's not installed."
}

_pylint_to_ve () {
    if [ -d /usr/lib/pymodules/python2.6/pylint ] && [ -d /usr/lib/pymodules/python2.6/logilab ]; then
        ln -sf /usr/lib/pymodules/python2.6/pylint $VIRTUALENVDIR/lib
        ln -sf /usr/lib/pymodules/python2.6/logilab $VIRTUALENVDIR/lib
    fi
}

if which virtualenv >/dev/null; then
    echo '  * Create virtualenv:'$VIRTUALENVDIR
    sudo virtualenv --no-site-packages $VIRTUALENVDIR
    _pylint_to_ve
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
    echo '  * Create link to supervisor conf:'$SUPERVISOR_CONFPATH
    sudo ln -sf $DEPLOY_DIR/deploy/supervisor.conf $SUPERVISOR_CONFPATH
else
    _require supervisor 
fi
