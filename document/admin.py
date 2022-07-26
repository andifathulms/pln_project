from django.contrib import admin
from .models import Document, DocSKAI, Macro, MacroData, MacroFile

admin.site.register(Document)
admin.site.register(DocSKAI)
admin.site.register(Macro)
admin.site.register(MacroData)
admin.site.register(MacroFile)