from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import CertificateMultiForm
from .models import Certificate


# Create your views here.
class UploadCertificate(LoginRequiredMixin, CreateView):
    template_name = 'certificates/certificate_form.html'
    form_class = CertificateMultiForm
    title = 'Add Custom Certificate'
    success_url = reverse_lazy('all-certificates')

    def form_valid(self, form):
        bundle = form['Bundle'].save(commit=False)
        key = form['Key'].save(commit=False)
        bundle_key = bundle.id
        key_key = key.id
        print(key_key)
        print(bundle_key)
        certificate = form['Certificate'].save(commit=False)
        bundle.save()
        key.save()
        certificate.save()
        certificate.bundle_upload = bundle
        certificate.key_upload = key
        certificate.save()
        # caddyfile_build()

        return redirect(reverse_lazy('all-certificates'))


class CreateCertificate(LoginRequiredMixin, CreateView):
    model = Certificate
    fields = ['cert_name', 'bundle_text', 'key_text']
    title = 'Add Custom Certificate'
    success_url = reverse_lazy('all-certificates')

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        # caddyfile_build()

        return redirect(reverse_lazy('all-certificates'))


class AllCertificate(LoginRequiredMixin, ListView):
    template_name = 'certificates/all_certificates.html'
    context_object_name = 'certificates'
    queryset = Certificate.objects.order_by('id')
    paginate_by = 10
    title = 'All Certificates'


class UpdateCertificate(LoginRequiredMixin, UpdateView):
    model = Certificate
    fields = ['cert_name', 'bundle_upload', 'key_upload', 'bundle_text', 'key_text']
    slug_field = 'cert_name'
    success_url = reverse_lazy('all-certificates')
    title = 'Update Certificate'

    def form_valid(self, form):
        certificate = form.save(commit=False)
        certificate.save()
        # caddy = caddyfile_build()
        return redirect(reverse_lazy('dashboard'))


class DeleteCertificate(LoginRequiredMixin, DeleteView):
    model = Certificate
    title = "Delete Certificate"
    success_url = reverse_lazy('all-certificates')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        self.object.bundle_upload.delete()
        self.object.key_upload.delete()
        self.object.delete()

        # caddy = caddyfile_build()
        return HttpResponseRedirect(self.get_success_url())
