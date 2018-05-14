#!/bin/sh bash
set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "You need sudo privileges to run this script"

echo 'Starting installer, please look out for the prompts. Always select yes.' \
     'Installing pre-requisites' \
     'you have 5 seconds to proceed...' \
     'or' \
     'hit Ctrl+C to quit' \
     -e "\n"
sleep 6

echo 'Installing dependencies...'
apt-get update && apt-get -y upgrade && apt-get -y install --no-install-recommends \
  python3 \
  python3-pip \
  python3-setuptools \
  python3-wheel \
  python3-dev \
  gcc \
  libssl1.0.0 \
  libffi6 \
  git \
  curl

echo 'Making the app directories...'
sleep 3
mkdir /apps

echo 'Cloning repository...'
sleep 3

cd /apps
git clone https://github.com/morph1904/TygerCaddy.git

mkdir -p /apps/TygerCaddy/sites \
      /apps/TygerCaddy/TygerCaddy/data \
      /apps/TygerCaddy/TygerCaddy/data/logs

touch /apps/TygerCaddy/TygerCaddy/data/caddyfile.conf
touch /apps/TygerCaddy/TygerCaddy/data/logs/caddy.txt
touch /apps/TygerCaddy/TygerCaddy/data/logs/uwsgi.txt

echo 'Installing Caddy...'
sleep 3
curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy

echo 'Creating folders, moving files, setting permissions...'
mkdir -p /etc/caddy \
         /etc/ssl/caddy \
         /var/www

cp /apps/TygerCaddy/caddy.service        /etc/systemd/system/caddy.service
cp /apps/TygerCaddy/uwsgi.service        /etc/systemd/system/uwsgi.service
cp /apps/TygerCaddy/caddy-reload.path    /etc/systemd/system/caddy-reload.path
cp /apps/TygerCaddy/caddy-reload.service /etc/systemd/system/caddy-reload.service

chown -R root:www-data /etc/caddy \
                       /etc/ssl/caddy
chown -R www-data:www-data /var/www
chown root:root /etc/systemd/system/caddy.service \
                /usr/local/bin/caddy
                
chmod -R 770 /etc/ssl/caddy
chmod -R 755 /var/www \
             /usr/local/bin/caddy \
             /apps
chmod -R 744 /etc/systemd/system/caddy.service \
             /etc/systemd/system/caddy-reload.path \
             /etc/systemd/system/caddy-reload.service \
             /etc/systemd/system/uwsgi.service

setcap 'cap_net_bind_service=+eip' /usr/local/bin/caddy

echo 'Setting up services to run on boot...'
sleep 3

systemctl daemon-reload
systemctl enable caddy.service
systemctl enable uwsgi.service

echo 'Setting up initial install...'
sleep 3

pip3 install -r /apps/TygerCaddy/TygerCaddy/requirements.txt

echo 'Installing TygerCaddy almost there!'
sleep 3

systemctl start uwsgi
systemctl start caddy

echo 'Install complete!, Enter the server IP in your chosen browser complete the install wizard.'
