from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings


# Create your views here.

class LogsIndex(LoginRequiredMixin, View):
    def get(self, request):
        project = settings.BASE_DIR
        path = project + '/data/logs/'
        caddylogpath = path + 'caddy.txt'
        uwsgilogpath = path + 'uwsgi.txt'

        caddylog = open(caddylogpath, 'r+')
        uwsgilog = open(uwsgilogpath, 'r+')


        caddy = caddylog.read()
        caddy.replace('\n', '<br>')
        caddylog.close()

        uwsgi = uwsgilog.read()
        uwsgi.replace('\n', '<br>')
        uwsgilog.close()

        context = {'caddy': caddy,
                   'uwsgi': uwsgi}
        template_name = "logs/logs_index.html"

        return render(request, template_name, context)
