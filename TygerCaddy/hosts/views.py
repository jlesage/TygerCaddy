from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .caddyfile import caddyfile_build
from .models import Host


# Create your views here.


class CreateHost(LoginRequiredMixin, CreateView):
    model = Host
    fields = ['host_name', 'root_path', 'tls', 'staging', 'custom_ssl', 'custom_certs', 'force_redirect_https']
    title = 'Add Host'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        host = form.save(commit=False)
        if not form.cleaned_data['tls']:
            if 'http://' not in form.cleaned_data['host_name']:
                host.host_name = 'http://' + form.cleaned_data['host_name']
        host.save()
        host.save_m2m()
        caddyfile_build()

        return redirect(reverse_lazy('dashboard'))


class AllHosts(LoginRequiredMixin, ListView):
    template_name = 'hosts/all_hosts.html'
    context_object_name = 'hosts'
    queryset = Host.objects.order_by('id')
    paginate_by = 10
    title = 'All Hosts'


class UpdateHost(LoginRequiredMixin, UpdateView):
    model = Host
    fields = ['host_name', 'root_path', 'tls', 'staging', 'custom_ssl', 'custom_certs', 'force_redirect_https']
    slug_field = 'host_name'
    success_url = reverse_lazy('dashboard')
    title = 'Update Host'

    def form_valid(self, form):
        host = form.save(commit=False)
        if not form.cleaned_data['tls']:
            if 'http://' not in form.cleaned_data['host_name']:
                host.host_name = 'http://' + form.cleaned_data['host_name']
        host.save()
        form.save_m2m()
        caddyfile_build()
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
        caddy = caddyfile_build()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def generate(request):
    run = caddyfile_build()
    html = "<html><body><h2>Caddyfile has been regenerated</h2></body></html>"
    return HttpResponse(html)
