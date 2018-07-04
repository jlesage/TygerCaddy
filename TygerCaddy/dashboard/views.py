from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import ListView, UpdateView, TemplateView

from hosts.models import Host

# Create your views here.


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/index.html'
    context_object_name = 'hosts'
    queryset = Host.objects.order_by('id')
    paginate_by = 10
    title = 'Dashboard'


class AngularView(TemplateView):
    template_name = 'dashboard/../templates/angular/index.html'
    title = 'Dashboard'


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'password']
    template_name = 'dashboard/pass-change.html'
