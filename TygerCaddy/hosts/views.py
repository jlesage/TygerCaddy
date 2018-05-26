from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .caddyfile import generate_caddyfile
from .models import Host


# Create your views here.


class CreateHost(LoginRequiredMixin, CreateView):
    model = Host
    fields = ['host_name', 'proxy', 'root_path', 'tls', 'staging']
    title = 'Add Host'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        host = form.save(commit=False)
        if not form.cleaned_data['tls']:
            if 'http://' not in form.cleaned_data['host_name']:
                host.host_name = 'http://' + form.cleaned_data['host_name']

        host.save()
        generate_caddyfile()

        return redirect(reverse_lazy('dashboard'))


class AllHosts(LoginRequiredMixin, ListView):
    template_name = 'hosts/all_hosts.html'
    context_object_name = 'hosts'
    queryset = Host.objects.order_by('id')
    paginate_by = 10
    title = 'All Hosts'


class UpdateHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['host_name', 'proxy', 'root_path', 'tls', 'staging']
    slug_field = 'host_name'
    success_url = reverse_lazy('dashboard')
    title = 'Update Host'

    def form_valid(self, form):
        host = form.save(commit=False)
        if not form.cleaned_data['tls']:
            if 'http://' not in form.cleaned_data['host_name']:
                host.host_name = 'http://' + form.cleaned_data['host_name']
        host.save()
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

