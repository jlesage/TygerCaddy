# VERSION 0.1
# AUTHOR:       Tyler Parisi <tyler@possumlodge.me>
# DESCRIPTION:  WebUI autoproxy with Caddy
# TO_BUILD:     docker build -t tygercaddy/tygercaddy .
# TO_RUN:       docker run -d -p 80:80 -p 443:443 --name tygercaddy tygercaddy/tygercaddy

FROM ubuntu:16.04

# update, install, and cleanup packages
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update && apt-get -y upgrade && apt-get -y install \
    zip \
    unzip \
    python3-dev \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    wget \
    git \
    curl && \
  apt-get clean autoclean && \
  apt-get autoremove && \
  rm -rf /var/lib/{apt,dpkg,cache,log} && \
# Install python3 packages
  pip3 install uwsgi

# Install application
RUN mkdir -p /apps && cd /apps && \
  git clone https://github.com/morph1904/TygerCaddy.git && \
  mkdir -p /apps/TygerCaddy/sites && \
  curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy

# Add any additional folders required, correct file permissions
RUN mkdir -p /etc/caddy && \
  mkdir -p /etc/ssl/caddy && \
  mkdir -p /var/www && \
  chown root:root /usr/local/bin/caddy && \
  chmod 755 /usr/local/bin/caddy && \
  setcap 'cap_net_bind_service=+eip' /usr/local/bin/caddy && \
  chown -R root:www-data /etc/caddy && \
  chown -R root:www-data /etc/ssl/caddy && \
  chmod 770 /etc/ssl/caddy && \
  chown www-data:www-data /var/www && \
  chmod 755 /var/www && \
  chmod -R 0775 /apps

# Finalize TygerCaddy install
RUN cd /apps/TygerCaddy/TygerCaddy && \
  /bin/bash -c 'mkdir -p /run/uwsgi; chown www-data:www-data /run/uwsgi' && \
  (/usr/local/bin/uwsgi --emperor /apps/TygerCaddy/uwsgi.ini) & \
  pip3 install -r /apps/TygerCaddy/TygerCaddy/requirements.txt

EXPOSE 80
EXPOSE 443

VOLUME ["/apps/TygerCaddy/sites/","/etc/ssl/caddy/"]

ENTRYPOINT ["entrypoint.sh"]
CMD ["run"]
