# -*- mode: shell-script -*-

# makesite show error
_makesite_error () {
    echo "ERROR: "$1 1>&2
}

# Verify that the SITES_HOME directory exists
_makesite_verify_sites_home () {
    if [ ! -d "$SITES_HOME" ]; then
        _makesite_error "Makesite sites directory '$SITES_HOME' does not exist.  Create it or set SITES_HOME to an existing directory."
        return 1
    fi
    return 0
}

# Verify that the requested site exists
_makesite_verify_site () {
    if [ ! -d "$1" ]; then
        _makesite_error "Project '$1' not found."
        return 1
    fi
    return 0
}

# List of available sites.
_makesite_find_sites () {
    _makesite_verify_sites_home || return 1
    find $SITES_HOME -maxdepth 3 -name '.makesite' | sed 's|/\.makesite||' | sort
}

# Get sitename
_sitename () {
    if [ -z "$1" ]; then
        return 1
    fi
    branch=`basename $1`
    project=`dirname $1 | xargs basename`
    echo -n $project"."$branch
}

# Show site info
_makesite_showinfo () {
    _sitename $1
    if [ -f "$1/.makesite" ]; then
        echo -n ' [' && cat "$1/.makesite" && echo ']'
    fi
}

# List sites
lssites () {
    sites=`_makesite_find_sites`
    for site in $sites; do
        _makesite_showinfo "$site"
    done
}

# View status sites
statsites () {
    sites=`_makesite_find_sites`
    for site in $sites; do
        sudo supervisorctl status `_sitename $site`
    done
}

# Change dir to site dir
cdsite () {
    project="$1"
    if [ -z "$1" ]; then
        _makesite_verify_sites_home || return 1
        cd $SITES_HOME
    else
        _makesite_verify_site $project || return 1
        cd $project
    fi
}

# View site log
logsite () {
    _makesite_verify_sites_home || return 1
    if [ -f "$1" ]; then
        tailf -n 50 $1
    else
        _makesite_error "Not found logfile '$log'."
    fi
}

# View site info
siteinfo () {
    _makesite_verify_sites_home || return 1
    _makesite_verify_site $1 || return 1
    _makesite_showinfo $1
    cat $1/makesite.ini
}

# Activate site virtualenv
envsite () {
    project="$1"
    if [ -z $project ]; then
        project=`echo $PWD | sed 's|/source$||'`
    fi
    activate=$project/.virtualenv/bin/activate

    _makesite_verify_sites_home || return 1
    _makesite_verify_site $project || return 1

    if [ ! -f "$activate" ]
    then
        _makesite_error "Project '`_makesite_showinfo $project`' does not contain an activate script."
        return 1
    fi

    source "$activate"

    # Path virtualenv bash promt
    if [ ! -z "$_OLD_VIRTUAL_PS1" ]; then
        PS1=(`_sitename $project`)$_OLD_VIRTUAL_PS1
        export PS1
    fi
}

# Cahnge dir to site source and activate virtualenv
worksite () {
    project="$1"
    cdsite $1
    envsite $1
    if [ -d $1/source ]; then
        cd $1/source
    fi
}

if [ -n "$BASH" ] ; then
    _sites ()
    {
        local cur="${COMP_WORDS[COMP_CWORD]}"
        COMPREPLY=( $(compgen -W "`_makesite_find_sites`" -- ${cur}) )
    }

    complete -o default -o nospace -F _sites cdsite
    complete -o default -o nospace -F _sites envsite
    complete -o default -o nospace -F _sites worksite
    complete -o default -o nospace -F _sites siteinfo
    complete -o default -o nospace -F _sites installsite
    complete -o default -o nospace -F _sites updatesite
    complete -o default -o nospace -F _sites removesite
    complete -o default -o nospace -F _sites testsite
    complete -o default -o nospace -F _sites logsite
fi
