import os
import time
import subprocess
from django.conf import settings
from .models import Host, Config
from django.contrib.auth.models import User


def generate_caddyfile():
    project = settings.BASE_DIR
    caddyfilepath = project + '/caddyfile.conf'

    caddyfile = open(caddyfilepath, "w+")

    user = User.objects.get(pk=1)
    host_set = Host.objects.all()
    config = Config.objects.get(pk=1)

    for caddyhost in host_set:
        if (caddyhost.tls == False):
            domain = caddyhost.host_name + ':80 { \n \n'
        else:
            domain = caddyhost.host_name + ' { \n \n'

        proxy = 'proxy / ' + caddyhost.proxy_host + ' { \n' \
                'transparent \n' \
                'insecure_skip_verify' \
                '  } \n'

        if caddyhost.tls:
            caddytls = 'tls ' + user.email + '\n } \n \n'
            caddyfile.write(domain + proxy + caddytls)
        else:
            proxy = proxy + '} \n \n'
            caddyfile.write(domain + proxy)
            caddyfile.close()

    caddyfile = open(caddyfilepath, "a")
    domain = config.interface + ' { \n \n'

    proxy = 'proxy / ' + config.proxy_host + ' { \n' \
                                             'transparent \n' \
                                             'except /assets \n' \
                                             '} \n \n'
    root = 'root /apps/TygerCaddy/TygerCaddy/ \n' \
           '} \n'
    caddyfile.write(domain + proxy + root)
    caddyfile.close()

    # with open(project + '/caddypid.txt', 'r') as caddyservice:
    #   caddypid = caddyservice.read().replace('\n', '')
    #  print(caddypid)

    # command = "kill -s USR1 " + caddypid
    # print(command)
    # reload = subprocess.run(command, shell=True)
    subprocess.call(['sudo', 'service', 'caddy', 'reload'])
    return True






