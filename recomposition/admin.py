from django.contrib import admin

from .models import UsulanRekomposisi, UsulanRekomposisiData, UsulanPeriod, EbudgetFile

admin.site.register(UsulanRekomposisi)
admin.site.register(UsulanRekomposisiData)
admin.site.register(UsulanPeriod)
admin.site.register(EbudgetFile)
