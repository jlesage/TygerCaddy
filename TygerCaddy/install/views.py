import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.shortcuts import render, redirect
from django.views.generic import View
from hosts.caddyfile import *
from config.models import Config


# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'install/install.html')

    def post(self, request):
        call_command('migrate')
        call_command('loaddata', 'dns')
        call_command('loaddata', 'variables')
        form = request.POST
        if form.get('dns-switch') == 'on':
            dns_check = True
        else:
            dns_check = False

        #  if not form['dns_provider']:
        #      dns_provider = ""
        #  else:
        # dns_provider = form['dns_provider']
        config = {
            'username': form['username'],
            'password': form['password'],
            'email': form['email'],
            'interface': form['listen_ip'],
            'port': form['listen_port'],
            'proxy-host': form['backend_proxy'],
            'dns-switch': dns_check,
            # 'dns-provider': dns_provider,
            'dash-colour': 'orange'
        }

        admin = User.objects.create_superuser(config['username'], config['email'], config['password'])
        new_config = Config(interface=config['interface'],
                            proxy_host=config['proxy-host'],
                            name='primary', port=config['port'],
                            proxy_exception='/assets',
                            root_dir=settings.BASE_DIR,
                            dns_challenge=dns_check,
                            )
        new_config.save()
        generate_keyfile()
        generate_dash()

        return redirect('login')


def generate_keyfile():
    chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"',
                                                                                                         '').replace(
        '\\', '')

    SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])
    keyfile = settings.BASE_DIR + '/data/secret.txt'

    key = open(keyfile, 'w+')
    key.write(SECRET_KEY)
    key.close()
    return True
