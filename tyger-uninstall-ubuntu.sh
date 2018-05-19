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

printf "Starting uninstaller\n" \
     "You have 5 before uninstallation begins...\n" \
     "or hit Ctrl+C to quit\n" \
     "\n"
sleep 6

printf "Stopping Services"

service uwsgi stop
service caddy stop

printf "Removing Python Packages..."

pip3 uninstall -y -r /apps/TygerCaddy/TygerCaddy/requirements.txt

printf "Removing TygerCaddy\n" \
     "WARNING! This will remove the whole /apps directory and all backups.\n" \
     "This is your last chance to cancel\n" \
     "You have 5 seconds to proceed...\n" \
     "or hit Ctrl+C to quit\n" \
     "\n"
sleep 6

rm -rf /usr/local/bin/caddy \
      /etc/caddy \
      /etc/ssl/caddy \
      /etc/systemd/system/caddy.service \
      /etc/systemd/system/caddy-reload.path \
      /etc/systemd/system/caddy-reload.service \
      /etc/systemd/system/uwsgi.service \
      /apps/TygerCaddy \
      /backup/TygerCaddy

apt remove -y uwsgi
systemctl daemon-reload


printf "Uninstall Complete!"

sleep 3
