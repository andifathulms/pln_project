from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

class not_found_404(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'snippets/not_found.html', {})