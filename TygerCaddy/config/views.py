from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, View
from .models import Config
from hosts.caddyfile import *


# Create your views here.
class UpdateConfig(LoginRequiredMixin, UpdateView):
    model = Config
    slug_field = 'name'
    template_name = 'config/config_form.html'
    fields = ['interface', 'port', 'proxy_host', 'proxy_exception', 'root_dir', 'dns_challenge', 'dns_provider']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.save()
        caddy = generate_caddyfile()
        if form.cleaned_data['dns_challenge']:
            return redirect(reverse_lazy('dns-challenge'))
        else:
            return redirect(reverse_lazy('dashboard'))


class VariableSet(View):

    def get(self, request):
        config = Config.objects.get(pk=1)
        if config.dns_challenge:
            variables = EVariables.objects.filter(dns_provider_id=config.dns_provider_id)
            return render(request, 'config/dns-challenge_form.html', {'variables': variables})
        else:
            return render(request, 'config/dns-challenge_error.html')

    def post(self, request):
        config = Config.objects.get(pk=1)
        variables = EVariables.objects.filter(dns_provider_id=config.dns_provider_id)

        for var in variables:
            form_value = request.POST.get(var.variable)
            print(form_value)
            value = EVariables.objects.get(pk=var.id)
            value.value = str(form_value)
            value.save()

        return redirect('/hosts/config/edit/primary')