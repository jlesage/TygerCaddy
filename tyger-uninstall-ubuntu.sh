#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo 'Starting uninstaller...'

sleep 3
echo 'You have 5 seconds to proceed ...'
echo 'or hit Ctrl+C to quit'
echo -e "\n"
sleep 6

echo 'Stopping Services'

service uwsgi stop
service caddy stop

echo 'Disabling Services'

rm -R /etc/systemd/system/uwsgi.service

echo 'Removing Python Packages...'
cd /apps/TygerCaddy/TygerCaddy
pip3 uninstall -y -r requirements.txt

echo 'Uninstalling Services'
sleep 3

apt remove -y uwsgi
rm -R /usr/local/bin/caddy
rm -R /etc/caddy
rm -R /etc/ssl/caddy
rm -R /etc/systemd/system/caddy.service
rm -R /etc/systemd/system/caddy-reload.path
rm -R /etc/systemd/system/caddy-reload.service

systemctl daemon-reload



echo 'Removing TygerCaddy'
echo 'WARNING! This will remove the whole /apps directory and all backups.'
echo 'This is your last chance to cancel'
echo 'You have 5 seconds to proceed ...'
echo 'or hit Ctrl+C to quit'
echo -e "\n"
sleep 6

cd /
rm -R /apps

echo Uninstall Complete!,

sleep 3





