from django.contrib import admin

from .models import DummyTable, DummyFileUpload

admin.site.register(DummyTable)
admin.site.register(DummyFileUpload)
