#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo 'Starting updater...'

sleep 3

echo 'Backing up config...'
echo 'You have 5 seconds to proceed ...'
echo 'or hit Ctrl+C to quit'
echo -e "\n"
sleep 6

echo 'Backing up DB and caddyfile'

mkdir /backup

cp /apps/TygerCaddy/TygerCaddy/db.sqlite3 /backup/db.sqlite3
cp /apps/TygerCaddy/TygerCaddy/caddyfile.conf /backup/caddyfile.conf

echo 'Taking services down'
service caddy stop
service uwsgi stop

echo 'Removing Directory...'
rm -R /apps

echo Cloning repository....
sleep 3

mkdir /apps
cd /apps
git clone https://github.com/morph1904/TygerCaddy.git
chmod -R 0777 /apps


echo 'Restoring config...'

cp /backup/db.sqlite3 /apps/TygerCaddy/TygerCaddy/db.sqlite3
cp /backup/caddyfile.conf /apps/TygerCaddy/TygerCaddy/caddyfile.conf

mv /backup/db.sqlite3 /backup/db.sqlite3.bak
mv /backup/caddyfile.conf /backup/caddyfile.conf.bak

echo Restarting base Services.....

service uwsgi start
service caddy start

echo Setting up initial install....


echo Install Complete!, Enter the server IP in your chosen browser and login.

sleep 3





