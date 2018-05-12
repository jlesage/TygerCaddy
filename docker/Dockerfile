# VERSION 0.1
# AUTHOR:       Tyler Parisi <tyler@possumlodge.me>
# DESCRIPTION:  WebUI autoproxy with Caddy
# TO_BUILD:     docker build -t tygercaddy/tygercaddy .

FROM ubuntu:16.04
ENV TYGER_ROOT=/apps/TygerCaddy/

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
  rm -rf /var/lib/{apt,dpkg,cache,log}

# Install application
RUN mkdir -p /apps && cd /apps && \
  git clone https://github.com/morph1904/TygerCaddy.git --depth 1 && \
  curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy && \
  cd $TYGER_ROOT/TygerCaddy && \
  pip3 install uwsgi && \
  pip3 install -r $TYGER_ROOT/TygerCaddy/requirements.txt

# Add any additional folders required, correct file permissions, initialize db
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
  chmod -R 0775 /apps && \
  python3 $TYGER_ROOT/TygerCaddy/manage.py migrate && \
  python3 $TYGER_ROOT/TygerCaddy/manage.py loaddata config && \
  python3 $TYGER_ROOT/TygerCaddy/manage.py loaddata dns && \
  python3 $TYGER_ROOT/TygerCaddy/manage.py loaddata variables

EXPOSE 80 443

VOLUME ["/apps/TygerCaddy/TygerCaddy","/etc/ssl/caddy/"]

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]
