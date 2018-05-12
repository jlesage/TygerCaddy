#!/bin/bash

TYGER_DIR=/apps/TygerCaddy/TygerCaddy

python3 $TYGER_DIR/manage.py migrate
python3 $TYGER_DIR/manage.py loaddata config
python3 $TYGER_DIR/manage.py loaddata dns
python3 $TYGER_DIR/manage.py loaddata variables

script="
from django.contrib.auth.models import User;
username = 'admin';
password = 'secret';
email = 'admin@example.com';
if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python3 $TYGER_DIR/manage.py shell

/usr/local/bin/uwsgi --emperor /apps/TygerCaddy/uwsgi.ini &
/usr/local/bin/caddy -log stdout -pidfile=$TYGER_DIR/caddypid.txt -agree=true -conf=$TYGER_DIR/caddyfile.conf -root=/var/tmp
