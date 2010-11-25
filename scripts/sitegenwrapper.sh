# -*- mode: shell-script -*-

# Verify that the SITES_HOME directory exists
_sitegen_verify_sites_home () {
    if [ ! -d "$SITES_HOME" ]
    then
        echo "ERROR: Sitegen sites directory '$SITES_HOME' does not exist.  Create it or set SITES_HOME to an existing directory." >&2
        return 1
    fi
    return 0
}

# Verify that the requested site exists
_sitegen_verify_site () {
    typeset project="$1"
    if [ ! -d "$project" ]
    then
       echo "ERROR: Project '`_sitegen_showsite $project`' does not exist." >&2
       return 1
    fi
    return 0
}

# List of available sites.
_sitegen_find_sites () {
    _sitegen_verify_sites_home || return 1
    ( for f in $SITES_HOME/*/*/.sitegen; do echo $f; done ) 2>/dev/null | \sed 's|/\.sitegen||' | \sed 's|\*/\*||' | \sort
}

# Get sitename
_sitename () {
    typeset site=$1
    echo -n $site | \sed 's|^/sites/||' | \sed 's|/|.|'
}

# Show site info
_sitegen_showsite () {
    typeset site=$1
    _sitename $site
    if [ -f $site/.sitegen ]; then
        echo -n ' [' && cat $site/.sitegen && echo ']'
    fi
}

# List sites
lssites () {
    _sitegen_verify_sites_home || return 1

    for site in $(_sitegen_find_sites)
    do
        _sitegen_showsite "$site"
    done
}

# View status sites
statsites () {
    for site in $(_sitegen_find_sites)
    do
        sudo supervisorctl status `_sitename $site`
    done
}

# Change dir to site dir
cdsite () {
    typeset project="$1"
    _sitegen_verify_sites_home || return 1
    if [ "$project" != "" ]; then
        _sitegen_verify_site $project || return 1
        cd $project
    else
        cd $SITES_HOME
    fi
}

logsite () {
    typeset project="$1"
    _sitegen_verify_sites_home || return 1
    if [ "$project" != "" ]; then
        _sitegen_verify_site $project || return 1
        cat $project
    else
        echo "Not found log '$project'."
    fi
}

# Activate site virtualenv
envsite () {
    typeset project="$1"
    _sitegen_verify_sites_home || return 1
    _sitegen_verify_site $project || return 1

    activate=$project/.virtualenv/bin/activate
    if [ ! -f "$activate" ]
    then
        echo "ERROR: Project '`_sitegen_showsite $project`' does not contain an activate script." >&2
        return 1
    fi

    type deactivate >/dev/null 2>&1
    if [ $? -eq 0 ]
    then
        deactivate
        unset -f deactivate >/dev/null 2>&1
    fi
    
    source "$activate"
}

if [ -n "$BASH" ] ; then
    _sites ()
    {
        local cur="${COMP_WORDS[COMP_CWORD]}"
        COMPREPLY=( $(compgen -W "`_sitegen_find_sites`" -- ${cur}) )
    }

    complete -o default -o nospace -F _sites cdsite
    complete -o default -o nospace -F _sites envsite
    complete -o default -o nospace -F _sites installsite
    complete -o default -o nospace -F _sites updatesite
    complete -o default -o nospace -F _sites removesite
    complete -o default -o nospace -F _sites testsite
    complete -o default -o nospace -F _sites logsite
fi

