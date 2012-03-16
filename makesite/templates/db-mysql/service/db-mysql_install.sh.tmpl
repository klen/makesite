#!/bin/bash

. $(dirname $0)/utils.sh

# Variables
DBUSER={{ db_user }}
DBPASSWORD={{ db_password }}
DBNAME={{ db_name }}

HOST={{ mysql_host }}
PORT={{ mysql_port }}
CLIENT="mysql"
USER={{ mysql_user }}
PASSWORD={{ mysql_password }}

if [ -z "$USER" ] || [ -z $HOST ] || [ -z $PASSWORD ]; then
    # pass
    echo "MySql some data not defined."
    exit 0
fi

SQL_CREATE_DB="CREATE DATABASE IF NOT EXISTS $DBNAME;"
SQL_CREATE_USER="CREATE USER '$DBUSER@localhost' IDENTIFIED BY '$DBPASSWORD';"
SQL_GRANT_ALL="GRANT ALL ON $DBNAME.* TO '$DBUSER';"
SQL_FLUSH="FLUSH PRIVILEGES;"

$CLIENT -u$USER -p$PASSWORD -e "${SQL_CREATE_DB}${SQL_CREATE_USER}${SQL_GRANT_ALL}${SQL_FLUSH}"
