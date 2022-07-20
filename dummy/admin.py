from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import DummyTable

admin.site.register(DummyTable)
