FROM solita/ubuntu-systemd:16.04

COPY gitlab/build/ubuntu/ubuntu-install.sh /ubuntu-install.sh
COPY gitlab/build/ubuntu/entrypoint.sh /entrypoint.sh
ADD  gitlab/test /test

EXPOSE 80 443 9090
CMD ["/entrypoint.sh"]
