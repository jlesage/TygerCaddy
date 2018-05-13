import os

from django.conf import settings
from django.contrib.auth.models import User
from dns.models import EVariables

from .models import Host
from config.models import Config


def generate_dash():
    project = settings.BASE_DIR
    caddyfilepath = project + '/data/caddyfile.conf'
    config = Config.objects.get(pk=1)

    block = config.interface + ':' + str(config.port) + ' { \n \n' \
                                                        'proxy / ' + config.proxy_host + ' { \n' \
                                                        'transparent \n' \
                                                        'except ' + config.proxy_exception + '\n' \
                                                        '} \n \n' \
                                                        'root ' + str(config.root_dir) + '\n' \
                                                        '} \n'

    caddyfile = open(caddyfilepath, "a")
    caddyfile.write(block)
    caddyfile.close()


def set_evariables(config, dns):
    variables = EVariables.objects.filter(dns_provider_id=dns.id)

    for var in variables:
        os.environ[var.variable] = str(var.value)
        print(os.environ[var.variable])


def generate_caddyfile():
    config = Config.objects.get(pk=1)
    if config.dns_provider:
        dns = config.dns_provider
        caddyname = dns.caddy_name
        set_evariables(config=config, dns=dns)
    project = settings.BASE_DIR
    caddyfilepath = project + '/data/caddyfile.conf'

    caddyfile = open(caddyfilepath, "w+")

    user = User.objects.get(pk=1)
    host_set = Host.objects.all()

    for caddyhost in host_set:
        block = caddyhost.host_name + ' { \n \n'
        proxy = 'proxy / ' + caddyhost.proxy_host + ' { \n' \
                                                    'transparent \n' \
                                                    'insecure_skip_verify \n' \
                                                    '  } \n'
        if caddyhost.tls == False:
            caddytls = 'tls off \n } \n \n'
        elif config.dns_challenge:
            caddytls = 'tls ' + caddyname + '\n } \n \n'
        else:
            caddytls = 'tls ' + user.email + '\n } \n \n'

        caddyfile.write(block + proxy + caddytls)

    caddyfile.close()
    generate_dash()
    # subprocess.call(['sudo', 'service', 'caddy', 'reload'])
    return True






