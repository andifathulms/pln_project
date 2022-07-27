from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Document, DocSKAI, MacroFile, Macro, MacroData
from .forms import DocumentForm

from itertools import chain

from tablib import Dataset

class SKAIListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        doc_skai = DocSKAI.objects.select_related('document')
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year

        return render(request, 'document/list_skai.html', context)
    
    def post(self, request, *args, **kwargs):
        pass

class LKAIListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        doc_skai = DocSKAI.objects.select_related('document')
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        return render(request, 'document/list_lkai.html', context)

    def post(self, request, *args, **kwargs):
        pass

class SKAIComparison(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'document/skai_comparison.html', context)


class UploadSKAI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        context["doc_skai"] = doc_skai
        return render(request, 'document/upload_SKAI.html', context)

    
    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'submit-skai' in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI(document=doc, year=request.POST['year'],revision=False)
                skai.save()
            else:
                print(doc.errors)
        elif 'submit-skai-rev' in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI(document=doc, year=request.POST['year'],revision=True,revision_number=request.POST['rev_number'])
                skai.save()
        
        doc_skai = DocSKAI.objects.all()
        context["doc_skai"] = list(chain(doc_skai))

        return render(request, 'document/upload_SKAI.html', context)

