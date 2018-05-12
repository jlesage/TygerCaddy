#!/bin/bash

TYGER_DIR=/apps/TygerCaddy/TygerCaddy

python3 $TYGER_DIR/manage.py migrate

script="
from django.contrib.auth.models import User;
username = '$username';
password = '$password';
email = '$email';
if User.objects.filter(username=username).count()==0:
    User.objects.create_superuser(username, email, password);
    print('Superuser created.');
else:
    print('Superuser creation skipped.');
"
printf "$script" | python3 $TYGER_DIR/manage.py shell

uwsgi --emperor /apps/TygerCaddy/uwsgi.ini &
caddy -log stdout -pidfile=$TYGER_DIR/caddypid.txt -agree=true -conf=$TYGER_DIR/caddyfile.conf -root=/var/tmp
