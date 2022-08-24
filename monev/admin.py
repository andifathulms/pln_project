from django.contrib import admin
from .models import LRPA_Monitoring, LRPA_File, Assigned_PRK, PRK_Lookup, FileMouPengalihan, MouPengalihanData

admin.site.register(LRPA_Monitoring)
admin.site.register(LRPA_File)
admin.site.register(Assigned_PRK)
admin.site.register(PRK_Lookup)
admin.site.register(FileMouPengalihan)
admin.site.register(MouPengalihanData)