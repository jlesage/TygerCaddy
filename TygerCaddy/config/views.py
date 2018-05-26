from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from hosts.caddyfile import *

from .models import Config


# Create your views here.
class UpdateConfig(LoginRequiredMixin, UpdateView):
    model = Config
    slug_field = 'name'
    template_name = 'config/config_form.html'
    fields = ['interface', 'port', 'proxy_host', 'proxy_exception', 'root_dir',
              'ssl_staging']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        caddy = generate_caddyfile()

        return redirect(reverse_lazy('dashboard'))
