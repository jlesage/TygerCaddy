import os
import subprocess

from config.models import Config
from django.conf import settings
from django.contrib.auth.models import User
from dns.models import EVariables
from proxies.models import Header, Proxy

from .models import Host


def reload_caddy():
    subprocess.call('pkill -USR1 caddy', shell=True)
    return True


def build_header_list(proxyID):
    # Get a list of associated custom header directives
    headerlist = Header.objects.filter(proxy_id=proxyID)
    headerblock =''
    # If the proxy has associated custom headers
    if headerlist:
        # For each of the header entries associated
        for header in headerlist:
            # If the header is a downstream header
            if header.downstream:
                # Build the downstream header value
                headerblock += 'header_downstream ' + header.header + ' ' + header.value + '\n'
            # If the header is a upstream header
            if header.upstream:
                # Build the upstream header value
                headerblock += 'header_upstream ' + header.header + ' ' + header.value + '\n'
        return headerblock
    else:
        return False


def build_proxy_block(hostID):
    # Get the associated proxies for the current host
    proxies = Proxy.objects.filter(host_id=hostID)
    if not proxies:
        # Make the block blank...
        return False
    else:
        proxyblock = ''
        print("Proxy block started")

        # For every proxy associated with this hostname
        for proxy in proxies:
            print("Generating proxy: ", proxy.name)
            # Build the proxy block based on the found values in the DB
            proxyblock += '\t\t proxy ' + proxy.proxy_from + ' ' + proxy.proxy_to + ' { \n'
            if proxy.load_policy:
                proxyblock += '\t\t\t load_policy ' + str(proxy.load_policy.name) + '\n'
            if proxy.fail_timeout:
                proxyblock += '\t\t\t fail_timeout ' + str(proxy.fail_timeout) + '\n'
            if proxy.max_fails:
                proxyblock += '\t\t\t max_fails ' + str(proxy.max_fails) + '\n'
            if proxy.max_conns:
                proxyblock += '\t\t\t max_conns ' + str(proxy.max_conns) + '\n'
            if proxy.try_duration:
                proxyblock += '\t\t\t try_duration ' + str(proxy.try_duration) + '\n'
            if proxy.try_interval:
                proxyblock += '\t\t\t try_interval ' + str(proxy.try_interval) + '\n'
            if proxy.health_check:
                proxyblock += '\t\t\t health_check ' + str(proxy.health_check) + '\n'
            if proxy.health_check_port:
                proxyblock += '\t\t\t health_check_port ' + str(proxy.health_check_port) + '\n'
            if proxy.health_check_interval:
                proxyblock += '\t\t\t health_check_interval ' + str(proxy.health_check_interval) + '\n'
            if proxy.health_check_timeout:
                proxyblock += '\t\t\t health_check_timeout ' + str(proxy.health_check_timeout) + '\n'
            if proxy.keep_alive:
                proxyblock += '\t\t\t keep_alive ' + str(proxy.keep_alive) + '\n'
            if proxy.timeout:
                proxyblock += '\t\t\t timeout ' + str(proxy.timeout) + '\n'
            if proxy.without:
                proxyblock += '\t\t\t without ' + str(proxy.without) + '\n'
            if proxy.exceptions:
                proxyblock += '\t\t\t exceptions ' + str(proxy.exceptions) + '\n'
            if proxy.insecure_skip_verify:
                proxyblock += '\t\t\t insecure_skip_verify \n'
            if proxy.websocket:
                proxyblock += '\t\t\t websocket \n'
            if proxy.transparent:
                proxyblock += '\t\t\t transparent \n'

            headerblock = build_header_list(proxyID=proxy.id)

            if headerblock:
                proxyblock += headerblock

            # Close off the proxyblock
            proxyblock += '\t\t } \n'
        print("Proxy block Ended")
        return proxyblock


def build_ssl_block(caddyhost):
    user = User.objects.get(pk=1)
    certblock = ''
    print("Cert block started")
    if not caddyhost.tls:
        certblock = '\ttls off \n } \n \n'

    if caddyhost.staging:
        certblock = '\ttls ' + user.email + ' {\n' \
                                            '\t ca https://acme-staging-v02.api.letsencrypt.org/directory\n' \
                                            '\t } \n' \
                                            '} \n'
    certs = caddyhost.custom_certs.all()
    if certs and caddyhost.custom_ssl:
        for cert in certs:
            certblock = '\ttls ' + os.path.join(cert.bundle_upload.bundle_file.path) + ' ' + os.path.join(
                cert.key_upload.key_file.path) + '\n } \n \n'
    else:
        certblock = '\ttls ' + user.email + '\n } \n \n'
    print("Cert block ended")
    return certblock


def build_host_block(caddyhost):
    # Start the host part of the block
    # Set the host name to respond to
    print("Host block started")
    print("Generating host: ", caddyhost.host_name)
    if caddyhost.force_redirect_https:
        proxyblock = caddyhost.host_name + ':443 { \n'
    else:
        proxyblock = caddyhost.host_name + ' { \n'
    # Add the root path
    proxyblock += '\t root ' + caddyhost.root_path + '\n'
    # Add the basic auth if defined.
    if caddyhost.basic_auth:
        proxyblock += '\t basicauth / ' + caddyhost.basic_username + ' ' + caddyhost.basic_password + '\n'
    proxyblock += build_proxy_block(hostID=caddyhost.id)
    print("Host block ended", caddyhost.host_name)
    return proxyblock


def caddyfile_build():

    project = settings.BASE_DIR
    caddyfilepath = project + '/data/caddyfile.conf'
    caddyfile = open(caddyfilepath, "w+")

    hosts = Host.objects.all()

    if hosts:
        block = ''
        for caddyhost in hosts:
            proxies = Proxy.objects.filter(host_id=caddyhost.id)
            if not proxies:
                block = ''
            else:
                block = build_host_block(caddyhost=caddyhost)
                ssl = build_ssl_block(caddyhost=caddyhost)
                block += ssl
                caddyfile.write(block)

    caddyfile.close()
    generate_dash()
    reload_caddy()

    return True

# def generate_caddyfile():
#     user = User.objects.get(pk=1)
#
#     project = settings.BASE_DIR
#     caddyfilepath = project + '/data/caddyfile.conf'
#     caddyfile = open(caddyfilepath, "w+")
#
#     config = Config.objects.get(pk=1)
#     if config.dns_provider:
#         dns = config.dns_provider
#         caddyname = dns.caddy_name
#         set_evariables(config=config, dns=dns)
#
#     hosts = Host.objects.all()
#     if hosts:
#         for caddyhost in hosts:
#             # if caddyhost.dns_verification:
#             # set_evariables(config=config, dns=caddyhost.dns_provider)
#
#             proxies = Proxy.objects.filter(host_id=caddyhost.id)
#             if not proxies:
#                 block = ''
#             else:
#                 block = caddyhost.host_name + ' { \n'
#                 block += '\t root ' + caddyhost.root_path + '\n'
#                 proxyblock = ''
#
#                 for proxy in proxies:
#                     headerlist = Header.objects.filter(proxy_id=proxy.id)
#
#                     proxyblock += '\t\t proxy ' + proxy.proxy_from + ' ' + proxy.proxy_to + ' { \n'
#                     if proxy.load_policy:
#                         proxyblock += '\t\t\t load_policy ' + str(proxy.load_policy.name) + '\n'
#                     if proxy.fail_timeout:
#                         proxyblock += '\t\t\t fail_timeout ' + str(proxy.fail_timeout) + '\n'
#                     if proxy.max_fails:
#                         proxyblock += '\t\t\t max_fails ' + str(proxy.max_fails) + '\n'
#                     if proxy.max_conns:
#                         proxyblock += '\t\t\t max_conns ' + str(proxy.max_conns) + '\n'
#                     if proxy.try_duration:
#                         proxyblock += '\t\t\t try_duration ' + str(proxy.try_duration) + '\n'
#                     if proxy.try_interval:
#                         proxyblock += '\t\t\t try_interval ' + str(proxy.try_interval) + '\n'
#                     if proxy.health_check:
#                         proxyblock += '\t\t\t health_check ' + str(proxy.health_check) + '\n'
#                     if proxy.health_check_port:
#                         proxyblock += '\t\t\t health_check_port ' + str(proxy.health_check_port) + '\n'
#                     if proxy.health_check_interval:
#                         proxyblock += '\t\t\t health_check_interval ' + str(proxy.health_check_interval) + '\n'
#                     if proxy.health_check_timeout:
#                         proxyblock += '\t\t\t health_check_timeout ' + str(proxy.health_check_timeout) + '\n'
#                     if proxy.keep_alive:
#                         proxyblock += '\t\t\t keep_alive ' + str(proxy.keep_alive) + '\n'
#                     if proxy.timeout:
#                         proxyblock += '\t\t\t timeout ' + str(proxy.timeout) + '\n'
#                     if proxy.without:
#                         proxyblock += '\t\t\t without ' + str(proxy.without) + '\n'
#                     if proxy.exceptions:
#                         proxyblock += '\t\t\t exceptions ' + str(proxy.exceptions) + '\n'
#                     if proxy.insecure_skip_verify:
#                         proxyblock += '\t\t\t insecure_skip_verify \n'
#                     if proxy.websocket:
#                         proxyblock += '\t\t\t websocket \n'
#                     if proxy.transparent:
#                         proxyblock += '\t\t\t transparent \n'
#
#                     if headerlist:
#                         for header in headerlist:
#                             if header.downstream:
#                                 proxyblock += 'header_downstream ' + header.header + ' ' + header.value + '\n'
#                             if header.upstream:
#                                 proxyblock += 'header_upstream ' + header.header + ' ' + header.value + '\n'
#
#                     proxyblock += '\t\t } \n'
#
#                 block += proxyblock
#
#                 if caddyhost.tls == False:
#                     block += '\ttls off \n } \n \n'
#                 elif config.dns_challenge:
#                     block += '\ttls ' + caddyname + '\n } \n \n'
#                 elif caddyhost.staging:
#                     block += '\ttls ' + user.email + ' {\n' \
#                                                      '\t ca https://acme-staging-v02.api.letsencrypt.org/directory\n' \
#                                                      '\t } \n' \
#                                                      '} \n'
#
#                 else:
#                     block += '\ttls ' + user.email + '\n } \n \n'
#
#             caddyfile.write(block)
#
#     caddyfile.close()
#     generate_dash()
#     reload_caddy()
#     return True


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

    caddyfile = open(caddyfilepath, "a+")
    caddyfile.write(block)
    caddyfile.close()

    return True


def set_evariables(config, dns):
    variables = EVariables.objects.filter(dns_provider_id=dns.id)
    project = settings.BASE_DIR
    envpath = project + '/data/dns.env'
    env = open(envpath, 'w+')

    for var in variables:
        line = var.variable + '=' + var.value + '\n'
        env.write(line)

    env.close()

    return True
