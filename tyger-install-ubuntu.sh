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

printf "Starting installer, please look out for the prompts. Always select yes.\n" \
     "Installing pre-requisites\n" \
     "you have 5 seconds to proceed...\n" \
     "or\n" \
     "hit Ctrl+C to quit\n" \
     "\n"
sleep 6

printf "Installing dependencies...\n"
apt-get update && apt-get -y upgrade && apt-get -y install --no-install-recommends \
  python3 \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  python3-dev \
  gcc \
  libssl-dev \
  libffi-dev \
  git \
  curl

printf "Making the app directories...\n"
sleep 3
mkdir /apps

printf "Cloning repository...\n"
sleep 3

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git

mkdir -p /apps/TygerCaddy/sites \
      /apps/TygerCaddy/TygerCaddy/data \
      /apps/TygerCaddy/TygerCaddy/data/logs

touch /apps/TygerCaddy/TygerCaddy/data/caddyfile.conf
touch /apps/TygerCaddy/TygerCaddy/data/logs/caddy.txt
touch /apps/TygerCaddy/TygerCaddy/data/logs/uwsgi.txt

printf "Installing Caddy...\n"
sleep 3
curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy

printf "Creating folders, moving files, setting permissions...\n"
mkdir -p /etc/caddy \
         /etc/ssl/caddy

cp /apps/TygerCaddy/caddy.service        /etc/systemd/system/caddy.service
cp /apps/TygerCaddy/uwsgi.service        /etc/systemd/system/uwsgi.service
cp /apps/TygerCaddy/caddy-reload.path    /etc/systemd/system/caddy-reload.path
cp /apps/TygerCaddy/caddy-reload.service /etc/systemd/system/caddy-reload.service

chown -R www-data:root /etc/caddy \
                       /etc/ssl/caddy
chown -R www-data:www-data /apps/TygerCaddy
chown root:root /etc/systemd/system/caddy.service \
                /etc/systemd/system/uwsgi.service \
                /etc/systemd/system/caddy-reload.path \
                /etc/systemd/system/caddy-reload.service \
                /usr/local/bin/caddy

chmod -R 700 /etc/ssl/caddy
chmod -R 755 /apps/TygerCaddy \
             /usr/local/bin/caddy \
             /etc/systemd/system/caddy.service \
             /etc/systemd/system/caddy-reload.path \
             /etc/systemd/system/caddy-reload.service \
             /etc/systemd/system/uwsgi.service

setcap 'cap_net_bind_service=+eip' /usr/local/bin/caddy

printf "Setting up services to run on boot...\n"
sleep 3

systemctl daemon-reload
systemctl enable caddy.service
systemctl enable uwsgi.service

printf "Setting up initial install...\n"
sleep 3

pip3 install -r /apps/TygerCaddy/TygerCaddy/requirements.txt

printf "Installing TygerCaddy almost there!\n"
sleep 3

systemctl start uwsgi
systemctl start caddy

printf "Install complete! Enter the server IP in your chosen browser complete the install wizard.\n"
