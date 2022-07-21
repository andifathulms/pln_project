from django.contrib import admin
from .models import Document, DocSKAI, DocAddedSKAI

admin.site.register(Document)
admin.site.register(DocSKAI)
admin.site.register(DocAddedSKAI)