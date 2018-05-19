#!/bin/bash

if [ "$(whoami)" != 'root' ]; then
  printf "This script must be run as "root".\n"
  printf "Enter password to elevate privileges:"
  printf "\n"
  SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
  SELF=`basename $0`
  sudo $SCRIPTPATH'/'$SELF
  exit 1
fi

printf "Starting updater...\n" \
     "Backing up config...\n" \
     "You have 5 seconds to proceed...\n" \
     "or hit Ctrl+C to quit\n" \
     "\n"
sleep 6

printf "Taking services down"

service caddy stop
service uwsgi stop

printf "Backing up DB and caddyfile"

mkdir -p /backup/TygerCaddy

cp /apps/TygerCaddy/TygerCaddy/db.sqlite3     /backup/TygerCaddy/db.sqlite3
cp /apps/TygerCaddy/TygerCaddy/caddyfile.conf /backup/TygerCaddy/caddyfile.conf

printf "Removing Directory..."
rm -R /apps/TygerCaddy

printf "Cloning repository..."
sleep 3

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git

printf "Restoring config..."

cp /backup/TygerCaddy/db.sqlite3     /apps/TygerCaddy/TygerCaddy/db.sqlite3
cp /backup/TygerCaddy/caddyfile.conf /apps/TygerCaddy/TygerCaddy/caddyfile.conf

mv /backup/TygerCaddy/db.sqlite3     /backup/TygerCaddy/db.sqlite3.bak
mv /backup/TygerCaddy/caddyfile.conf /backup/TygerCaddy/caddyfile.conf.bak

chmod -R 0775 /apps/TygerCaddy

printf "Restarting base Services..."

service uwsgi start
service caddy start

printf "Setting up initial install..."
cd /apps/TygerCaddy/TygerCaddy
pip3 install -r requirements.txt
python3 manage.py migrate

printf "Update complete!, Enter the server IP in your chosen browser and login."

sleep 3
