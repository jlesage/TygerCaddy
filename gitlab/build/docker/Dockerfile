FROM alpine:3.7
LABEL maintainer "Tyler Parisi <tyer@possumlodge.me>"

ENV APPS_DIR=/apps
ENV TYGER_ROOT=$APPS_DIR/TygerCaddy
ENV TYGER_DIR=$TYGER_ROOT/TygerCaddy
ENV TYGER_DATA=$TYGER_DIR/data
ENV TYGER_LOGS=$TYGER_DATA/logs
#######################
ARG CI_REPOSITORY_URL
ARG CI_COMMIT_REF_NAME
#######################
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
    libffi \
    ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install uwsgi

# Install application
RUN mkdir -p $APPS_DIR && cd $APPS_DIR && \
######################################
    git clone $CI_REPOSITORY_URL && \
    cd $TYGER_ROOT && \
    git checkout -qf $CI_COMMIT_REF_NAME && \
######################################
    pip3 install -r $TYGER_DIR/requirements.txt

# install caddy
RUN curl https://getcaddy.com | bash -s personal hook.service

# validate install
RUN caddy --version

# Add any additional folders required, correct file permissions
RUN mkdir -p $TYGER_DATA && \
    chmod -R 0775 $TYGER_ROOT

EXPOSE 80 443 9090

VOLUME ["/apps/TygerCaddy/TygerCaddy/data", "/root/.caddy"]

COPY docker/entrypoint.sh /entrypoint.sh
######################
ADD gitlab/test /test
######################
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run"]

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="TygerCaddy" \
      org.label-schema.description="Caddy based reverse proxy app with web GUI " \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version=$VERSION \
      org.label-schema.vcs-url="https://github.com/morph1904/TygerCaddy"
