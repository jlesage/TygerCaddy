from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .caddyfile import generate_caddyfile

from .models import Host, Config
from dns.models import DNS, EVariables

# Create your views here.


class CreateHost(LoginRequiredMixin, CreateView):
    model = Host
    fields = ['host_name', 'proxy_host', 'root_path', 'tls']
    title = 'Add Host'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        form.save()
        caddy = generate_caddyfile()
        return redirect(reverse_lazy('dashboard'))


class UpdateHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['host_name', 'proxy_host', 'root_path', 'tls']
    slug_field = 'host_name'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        form.save()
        caddy = generate_caddyfile()
        return redirect(reverse_lazy('dashboard'))


class DeleteHost(LoginRequiredMixin, DeleteView):
    model = Host
    title = "Delete Host"
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        caddy = generate_caddyfile()
        return HttpResponseRedirect(self.get_success_url())


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


@login_required
def generate(request):
    run = generate_caddyfile()
    return redirect('/dashboard')


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
