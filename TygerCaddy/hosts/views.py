from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .caddyfile import generate_caddyfile

from .models import Host
from config.models import Config
from dns.models import DNS, EVariables

# Create your views here.


class CreateHost(LoginRequiredMixin, CreateView):
    model = Host
    fields = ['host_name', 'proxy', 'root_path', 'tls']
    title = 'Add Host'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):

        form.save()
        caddy = generate_caddyfile()
        return redirect(reverse_lazy('dashboard'))


class AllHosts(LoginRequiredMixin, ListView):
    template_name = 'hosts/all_hosts.html'
    context_object_name = 'hosts'
    queryset = Host.objects.order_by('id')
    paginate_by = 10
    title = 'All Hosts'


class UpdateHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['host_name', 'proxy', 'root_path', 'tls']
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


@login_required
def generate(request):
    run = generate_caddyfile()
    return redirect('/dashboard')

