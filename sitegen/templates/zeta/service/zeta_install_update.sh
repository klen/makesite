ZETA_STATICDIR={{ project_staticdir }}

# Check zeta-library
which zeta 1>/dev/null || { echo "ERROR: * I require zeta but it's not installed."; exit 0; }

zeta $ZETA_STATICDIR
