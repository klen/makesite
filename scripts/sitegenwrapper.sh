# -*- mode: shell-script -*-

# Sitegen show error
_sitegen_error () {
    echo "ERROR: "$1 1>&2
}

# Verify that the SITES_HOME directory exists
_sitegen_verify_sites_home () {
    if [ ! -d "$SITES_HOME" ]; then
        _sitegen_error "Sitegen sites directory '$SITES_HOME' does not exist.  Create it or set SITES_HOME to an existing directory."
        return 1
    fi
    return 0
}

# Verify that the requested site exists
_sitegen_verify_site () {
    if [ ! -d "$1" ]; then
        _sitegen_error "Project '$1' not found."
        return 1
    fi
    return 0
}

# List of available sites.
_sitegen_find_sites () {
    _sitegen_verify_sites_home || return 1
    find $SITES_HOME -name '.sitegen' | sed 's|/\.sitegen||' | sort
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
_sitegen_showinfo () {
    _sitename $1
    if [ -f "$1/.sitegen" ]; then
        echo -n ' [' && cat "$1/.sitegen" && echo ']'
    fi
}

# List sites
lssites () {
    sites=`_sitegen_find_sites`
    for site in $sites; do
        _sitegen_showinfo "$site"
    done
}

# View status sites
statsites () {
    sites=`_sitegen_find_sites`
    for site in $sites; do
        sudo supervisorctl status `_sitename $site`
    done
}

# Change dir to site dir
cdsite () {
    project="$1"
    if [ -z "$1" ]; then
        _sitegen_verify_sites_home || return 1
        cd $SITES_HOME
    else
        _sitegen_verify_site $project || return 1
        cd $project
    fi
}

# View site log
logsite () {
    _sitegen_verify_sites_home || return 1
    if [ -f "$1" ]; then
        tailf -n 50 $1
    else
        _sitegen_error "Not found logfile '$log'."
    fi
}

# View site info
siteinfo () {
    _sitegen_verify_sites_home || return 1
    _sitegen_verify_site $1 || return 1
    _sitegen_showinfo $1
    cat $1/.project.ini
}

# Activate site virtualenv
envsite () {
    project="$1"
    activate=$project/.virtualenv/bin/activate

    _sitegen_verify_sites_home || return 1
    _sitegen_verify_site $project || return 1

    if [ ! -f "$activate" ]
    then
        _sitegen_error "Project '`_sitegen_showinfo $project`' does not contain an activate script."
        return 1
    fi

    source "$activate"

    # Path virtualenv bash promt
    if [ ! -z "$_OLD_VIRTUAL_PS1" ]; then
        PS1=(`_sitename $project`)$_OLD_VIRTUAL_PS1
        export PS1
    fi
}

if [ -n "$BASH" ] ; then
    _sites ()
    {
        local cur="${COMP_WORDS[COMP_CWORD]}"
        COMPREPLY=( $(compgen -W "`_sitegen_find_sites`" -- ${cur}) )
    }

    complete -o default -o nospace -F _sites cdsite
    complete -o default -o nospace -F _sites envsite
    complete -o default -o nospace -F _sites siteinfo
    complete -o default -o nospace -F _sites installsite
    complete -o default -o nospace -F _sites updatesite
    complete -o default -o nospace -F _sites removesite
    complete -o default -o nospace -F _sites testsite
    complete -o default -o nospace -F _sites logsite
fi

