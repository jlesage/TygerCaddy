from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, View

from .models import DNS, EVariables


# Create your views here.
class Providers(LoginRequiredMixin, ListView):
    template_name = 'dns/all_providers.html'
    context_object_name = 'dns'
    queryset = DNS.objects.order_by('id')
    paginate_by = 10
    title = 'All DNS Providers'


class SetVariables(LoginRequiredMixin, View):
    def get(self, request, dns):

        if dns:
            provider = DNS.objects.get(provider_name=dns)
            variables = EVariables.objects.filter(dns_provider_id=provider.id)
            return render(request, 'dns/dns-challenge_form.html', {'variables': variables})
        else:
            return render(request, 'dns/dns-challenge_error.html')

    def post(self, request, dns):
        provider = DNS.objects.get(provider_name=dns)
        variables = EVariables.objects.filter(dns_provider_id=provider.id)

        for var in variables:
            form_value = request.POST.get(var.variable)
            print(form_value)
            value = EVariables.objects.get(pk=var.id)
            value.value = str(form_value)
            value.save()

        return redirect('/hosts/list/')
