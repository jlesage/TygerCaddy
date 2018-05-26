#!/bin/bash

# Set used terminal colors
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

printf "${GREEN}You are about to update TygerCaddy.${NORMAL}\n"
read -p "${LIME_YELLOW}Proceed? (y/N)${NORMAL} " -r
printf "\n"
if [[ ! $REPLY =~ ^[Yy*] ]]
then
    exit
fi

printf "${GREEN}Taking services down...${NORMAL}\n"
systemctl stop caddy
systemctl stop uwsgi

printf "${GREEN}Backing up DB and caddyfile...${NOMAL}\n"
mkdir -p $TYGER_BACKUP

cp $TYGER_DATA/db.sqlite3     $TYGER_BACKUP/db.sqlite3
cp $TYGER_DATA/caddyfile.conf $TYGER_BACKUP/caddyfile.conf
cp $TYGER_LOGS/caddy.txt      $TYGER_BACKUP/caddy.txt
cp $TYGER_LOGS/uwsgi.txt      $TYGER_BACKUP/uwsgi.txt

printf "${GREEN}Removing old TygerCaddy install...${NORMAL}\n"
rm -R $TYGER_ROOT

printf "${GREEN}Cloning latest release...${NORMAL}\n"
cd $APPS_DIR
git clone https://github.com/morph1904/TygerCaddy.git

printf "${GREEN}Restoring config...${NORMAL}\n"
cp $TYGER_BACKUP/db.sqlite3     $TYGER_DATA/db.sqlite3
cp $TYGER_BACKUP/caddyfile.conf $TYGER_DATA/caddyfile.conf

mkdir -p $TYGER_LOGS
cp $TYGER_BACKUP/caddy.txt      $TYGER_LOGS/caddy.txt
cp $TYGER_BACKUP/uwsgi.txt      $TYGER_LOGS/uwsgi.txt

mv $TYGER_BACKUP/db.sqlite3     $TYGER_BACKUP/db.sqlite3.bak
mv $TYGER_BACKUP/caddyfile.conf $TYGER_BACKUP/caddyfile.conf.bak

rm $TYGER_BACKUP/caddy.txt \
   $TYGER_BACKUP/uwsgi.txt

chmod -R 0775 $TYGER_ROOT

printf "${GREEN}Restarting base Services...${NORMAL}\n"
systemctl start uwsgi
systemctl start caddy

printf "${GREEN}Setting up initial install...${NORMAL}\n"
cd $TYGER_DIR
pip3 install -r requirements.txt
python3 manage.py migrate

printf "${GREEN}Update complete! Enter the server IP in your chosen browser and login${NORMAL}\n"
