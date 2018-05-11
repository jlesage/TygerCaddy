#!/bin/bash

python3 manage.py migrate
python3 manage.py loaddata config
python3 manage.py loaddata dns
python3 manage.py loaddata variables

/usr/local/bin/uwsgi --emperor /apps/TygerCaddy/uwsgi.ini &
/usr/local/bin/caddy -log stdout -pidfile=/apps/TygerCaddy/TygerCaddy/caddypid.txt -agree=true -conf=/apps/TygerCaddy/TygerCaddy/caddyfile.conf -root=/var/tmp
