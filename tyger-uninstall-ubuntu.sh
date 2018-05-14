#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "You need sudo privileges to run this script"

echo 'Starting uninstaller' \
     'You have 5 before uninstallation begins...' \
     'or hit Ctrl+C to quit' \
     -e "\n"
sleep 6

echo 'Stopping Services'

service uwsgi stop
service caddy stop

echo 'Removing Python Packages...'

pip3 uninstall -y -r /apps/TygerCaddy/TygerCaddy/requirements.txt

echo 'Uninstalling Services'
sleep 3

apt remove -y uwsgi
rm -rf /usr/local/bin/caddy \
      /etc/caddy \
      /etc/ssl/caddy \
      /etc/systemd/system/caddy.service \
      /etc/systemd/system/caddy-reload.path \
      /etc/systemd/system/caddy-reload.service \
      /etc/systemd/system/uwsgi.service

systemctl daemon-reload

echo 'Removing TygerCaddy' \
     'WARNING! This will remove the whole /apps directory and all backups.' \
     'This is your last chance to cancel' \
     'You have 5 seconds to proceed ...' \
     'or hit Ctrl+C to quit' \
     -e "\n"
sleep 6

rm -rf /apps/TygerCaddy \
       /backup/TygerCaddy

echo Uninstall Complete!,

sleep 3
