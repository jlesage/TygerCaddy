#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "You need sudo privileges to run this script"

echo 'Starting updater...' \
     'Backing up config...' \
     'You have 5 seconds to proceed...' \
     'or hit Ctrl+C to quit' \
     -e "\n"
sleep 6

echo 'Taking services down'

service caddy stop
service uwsgi stop

echo 'Backing up DB and caddyfile'

mkdir -p /backup/TygerCaddy

cp /apps/TygerCaddy/TygerCaddy/db.sqlite3     /backup/TygerCaddy/db.sqlite3
cp /apps/TygerCaddy/TygerCaddy/caddyfile.conf /backup/TygerCaddy/caddyfile.conf

echo 'Removing Directory...'
rm -R /apps/TygerCaddy

echo 'Cloning repository...'
sleep 3

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git

echo 'Restoring config...'

cp /backup/TygerCaddy/db.sqlite3     /apps/TygerCaddy/TygerCaddy/db.sqlite3
cp /backup/TygerCaddy/caddyfile.conf /apps/TygerCaddy/TygerCaddy/caddyfile.conf

mv /backup/TygerCaddy/db.sqlite3     /backup/TygerCaddy/db.sqlite3.bak
mv /backup/TygerCaddy/caddyfile.conf /backup/TygerCaddy/caddyfile.conf.bak

chmod -R 0775 /apps/TygerCaddy

echo 'Restarting base Services...'

service uwsgi start
service caddy start

echo 'Setting up initial install...'
cd /apps/TygerCaddy/TygerCaddy
pip3 install -r requirements.txt
python3 manage.py migrate

echo 'Update complete!, Enter the server IP in your chosen browser and login.'

sleep 3
