PGUSER={{ pguser }}
PGPASSWORD={{ pgpassword }}
PGHOST={{ pghost }}
PSQL="psql -At"
DBNAME={{ project.replace('-', '_') }}_master
DBUSER={{ project.replace('-', '_') }}
DBPASSWORD={{ project.replace('-', '_') }}

export PGUSER=$PGUSER
export PGPASSWORD=$PGPASSWORD
export PGHOST=$PGHOST

SQL_CREATE_DB="create database $DBNAME with owner $DBUSER"
SQL_CREATE_ROLE="create role $DBUSER with login password '$DBPASSWORD'"
SQL_CHECK_DB="select count(1) from pg_catalog.pg_database where datname = '$DBNAME' "

_check_db_exist () {
    $PSQL -c "$SQL_CHECK_DB"
}

_create_role () {
    echo "  * Create user $DBUSER."
    $PSQL -c "$SQL_CREATE_ROLE"
}

_create_db () {
    echo "  * Create database $DBNAME."
    $PSQL -c "$SQL_CREATE_DB"
}

if [ $(_check_db_exist) -eq 0 ]; then
    _create_role
    _create_db
else
    echo "  * Database $DBNAME exist."
fi
