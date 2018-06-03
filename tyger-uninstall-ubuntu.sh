#!/bin/bash

# Set used terminal colors
RED=$(tput setaf 1)
BLINK=$(tput blink)
GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)
LIME_YELLOW=$(tput setaf 190)

# do not change, these are hardcoded elsewhere
APPS_DIR=/apps
BACKUP_DIR=/backup
TYGER_ROOT=$APPS_DIR/TygerCaddy
TYGER_DIR=$TYGER_ROOT/TygerCaddy
TYGER_DATA=$TYGER_DIR/data
TYGER_LOGS=$TYGER_DATA/logs
TYGER_BACKUP=$BACKUP_DIR/TygerCaddy

if [ "$(whoami)" != 'root' ]; then
  printf "${GREEN}This script must be run as \"root\"${NORMAL}\n"
  printf "\n"
  SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
  SELF=`basename $0`
  sudo $SCRIPTPATH'/'$SELF
  exit 1
fi

printf "${RED}You are about to uninstall TygerCaddy${NORMAL}\n"
read -p "${LIME_YELLOW}Proceed? (y/N)${NORMAL} " -r
printf "\n"
if [[ ! $REPLY =~ ^[Yy*] ]]
then
    exit 1
fi

printf "${GREEN}Stopping and removing services...${NORMAL}\n"
service uwsgi stop
service caddy stop

rm -rf /usr/local/bin/caddy \
       /etc/systemd/system/caddy.service \
       /etc/systemd/system/uwsgi.service

apt remove -y uwsgi
systemctl daemon-reload

printf "${GREEN}Remove Python packages?${NORMAL} "
read -p "${LIME_YELLOW}(y/N)${NORMAL} " -r
printf "\n"
if [[ $REPLY =~ ^[Yy*] ]]
  then
    pip3 uninstall -y -r $TYGER_DIR/requirements.txt
fi

printf "${RED}${BLINK}About to uninstall all user data${NORMAL}\n"
read -p "${RED}Proceed? (y/N)${NORMAL} " -r
printf "\n"
if [[ $REPLY =~ ^[Yy*] ]]
  then
    rm -rf /etc/caddy \
           /etc/ssl/caddy \
           $TYGER_ROOT \
           $TYGER_BACKUP
fi

printf "${GREEN}Uninstall Complete!${NORMAL}\n"
