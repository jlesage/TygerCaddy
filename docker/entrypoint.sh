#!/bin/bash

TYGER_DIR=/apps/TygerCaddy/TygerCaddy

if [ -e $TYGER_DIR/TygerCaddy/data/db.sqlite3 ]
then
  python3 $TYGER_DIR/manage.py migrate
else
  echo "Assuming new install, doing nothing"
fi

uwsgi --emperor /apps/TygerCaddy/uwsgi.ini &
caddy -log stdout -pidfile=$TYGER_DIR/caddypid.txt -agree=true -conf=$TYGER_DIR/caddyfile.conf -root=/var/tmp
