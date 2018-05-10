import os
import time
import subprocess
from django.conf import settings
from .models import Host, Config
from django.contrib.auth.models import User


def generate_dash():
    project = settings.BASE_DIR
    caddyfilepath = project + '/caddyfile.conf'
    config = Config.objects.get(pk=1)

    block = config.interface + ':' + str(config.port) + ' { \n \n' \
                                                        'proxy / ' + config.proxy_host + ' { \n' \
                                                                                         'transparent \n' \
                                                                                         'except ' + config.proxy_exception + '\n' \
                                                                                                                              '} \n \n' \
                                                                                                                              'root ' + str(
        config.root_dir) + '\n' \
                           '} \n'

    caddyfile = open(caddyfilepath, "a")
    caddyfile.write(block)
    caddyfile.close()


def generate_caddyfile():
    project = settings.BASE_DIR
    caddyfilepath = project + '/caddyfile.conf'

    caddyfile = open(caddyfilepath, "w+")

    user = User.objects.get(pk=1)
    host_set = Host.objects.all()

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

    generate_dash()
    # subprocess.call(['sudo', 'service', 'caddy', 'reload'])
    return True






