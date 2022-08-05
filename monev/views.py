from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

class MonevView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'monev/monev_lkai.html', context)
