FROM solita/ubuntu-systemd:16.04

COPY travis/install/baremetal.sh /baremetal.sh
COPY travis/docker/entrypoint.sh /entrypoint.sh

EXPOSE 80 443 9090
CMD ["/entrypoint.sh"]
