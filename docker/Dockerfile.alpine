# VERSION 0.1
# AUTHOR:       Tyler Parisi <tyler@possumlodge.me>
# DESCRIPTION:  WebUI autoproxy with Caddy
# TO_BUILD:     docker build -t morph1904/tygercaddy .

FROM alpine:latest
ENV TYGER_ROOT=/apps/TygerCaddy

# Install dependencies
RUN apk add --no-cache \
    git \
    curl \
    python3 \
    python3-dev \
    bash \
    gcc \
    libc-dev \
    linux-headers \
    openssl-dev \
    libffi && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools

# Install application
RUN mkdir -p /apps && cd /apps && \
    git clone https://github.com/morph1904/TygerCaddy.git --depth 1 && \
    curl https://getcaddy.com | bash -s personal hook.service,http.filemanager,http.jwt,http.mailout,http.minify,http.proxyprotocol,http.upload,net,tls.dns.godaddy && \
    cd TygerCaddy && \
    pip3 install uwsgi && \
    pip3 install -r $TYGER_ROOT/TygerCaddy/requirements.txt

# Add any additional folders required, correct file permissions
RUN mkdir -p /etc/ssl/caddy && \
    mkdir -p $TYGER_ROOT/TygerCaddy/data && \
    chmod -R 0775 /apps/TygerCaddy



EXPOSE 80 443 9090

VOLUME ["/apps/TygerCaddy/TygerCaddy/data","/etc/ssl/caddy/"]

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]
