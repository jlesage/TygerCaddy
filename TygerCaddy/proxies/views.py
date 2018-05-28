from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from hosts.caddyfile import generate_caddyfile
from hosts.models import Host

from .models import Header, Proxy


class CreateProxy(LoginRequiredMixin, CreateView):
    template_name = 'proxies/add_proxy.html'
    model = Proxy
    success_url = '/proxies/list'
    fields = ['name',
              'proxy_from',
              'proxy_to',
              'host',
              'load_policy',
              'fail_timeout',
              'max_fails',
              'max_conns',
              'try_duration',
              'try_interval',
              'health_check',
              'health_check_port',
              'health_check_interval',
              'health_check_timeout',
              'keep_alive',
              'timeout',
              'without',
              'exceptions',
              'insecure_skip_verify',
              'websocket',
              'transparent']
    hosts = Host.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super(CreateProxy, self).get_context_data(**kwargs)
        ctx['hosts'] = self.hosts
        return ctx

    def form_valid(self, form):
        form.save()
        generate_caddyfile()
        return redirect(reverse_lazy('all-proxies'))


class ListProxies(LoginRequiredMixin, ListView):
    template_name = 'proxies/all_proxies.html'
    context_object_name = 'proxies'
    queryset = Proxy.objects.order_by('id')
    paginate_by = 10
    title = 'All Proxies'


class DetailProxy(LoginRequiredMixin, DetailView):
    template_name = 'proxies/proxy_detail.html'
    title = 'Proxy Detail'
    model = Proxy


class UpdateProxy(LoginRequiredMixin, UpdateView):
    model = Proxy
    template_name = 'proxies/proxy_form.html'
    success_url = reverse_lazy('all-proxies')
    fields = ['name',
              'host',
              'proxy_from',
              'proxy_to',
              'load_policy',
              'fail_timeout',
              'max_fails',
              'max_conns',
              'try_duration',
              'try_interval',
              'health_check',
              'health_check_port',
              'health_check_interval',
              'health_check_timeout',
              'keep_alive',
              'timeout',
              'without',
              'exceptions',
              'insecure_skip_verify',
              'websocket',
              'transparent']

    def form_valid(self, form):
        form.save()
        generate_caddyfile()
        return redirect(reverse_lazy('all-proxies'))


class DeleteProxy(LoginRequiredMixin, DeleteView):
    model = Proxy
    title = "Delete Proxy"
    success_url = reverse_lazy('all-proxies')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        generate_caddyfile()
        return HttpResponseRedirect(self.get_success_url())


class CreateHeader(LoginRequiredMixin, CreateView):
    template_name = 'proxies/headers/add_header.html'
    model = Header
    success_url = '/proxies/headers/list'
    fields = ['header',
              'upstream',
              'downstream',
              'value',
              'proxy']
    def form_valid(self, form):

        form.save()
        generate_caddyfile()
        return redirect(reverse_lazy('all-headers'))


class ListHeaders(LoginRequiredMixin, ListView):
    template_name = 'proxies/headers/all_headers.html'
    context_object_name = 'headers'
    queryset = Header.objects.order_by('id')
    paginate_by = 10
    title = 'All Headers'


class DetailHeader(LoginRequiredMixin, DetailView):
    template_name = 'proxies/headers/header_detail.html'
    title = 'Header Detail'
    model = Proxy


class UpdateHeader(LoginRequiredMixin, UpdateView):
    model = Header
    fields = ['header',
              'upstream',
              'downstream',
              'value',
              'proxy']
    slug_field = 'header'
    success_url = reverse_lazy('all-headers')

    def form_valid(self, form):

        form.save()

        return redirect(reverse_lazy('all-headers'))


class DeleteHeader(LoginRequiredMixin, DeleteView):
    model = Header
    title = "Delete Header"
    template_name = 'proxies/headers/header_confirm_delete.html'
    success_url = reverse_lazy('all-headers')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.delete()
        generate_caddyfile()
        return HttpResponseRedirect(self.get_success_url())
