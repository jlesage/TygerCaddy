import os
from pathlib import Path

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy


class InstallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        install_settings = Path(os.path.join(settings.BASE_DIR, 'data/db.sqlite3'))
        print(request.path_info)
        if not install_settings.exists():
            if not request.path_info == '/install/':
                return redirect(reverse_lazy('install'))
