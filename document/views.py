from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView

from .models import Document, DocSKAI, MacroFile, Macro, MacroData
from .forms import DocumentForm

from itertools import chain

from tablib import Dataset
from django.utils import timezone

class SKAIListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        today = timezone.now()
        doc_skai = DocSKAI.objects.select_related('document').filter(document__published_date__year=today.year)
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year
        return render(request, 'document/list_skai.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.select_related('document').filter(document__published_date__year=request.POST["year"])
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year
        return render(request, 'document/list_skai.html', context)

class SKAIDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DocSKAI
    template_name = 'document/skai_delete.html'
    success_url = reverse_lazy('document:doc-list-skai')

    def test_func(self):
       return True #BIG WARNING

class SKAIUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        skai = DocSKAI.objects.get(pk=pk)
        context["skai"] = skai
        context["str_date"] = skai.document.published_date.strftime('%Y-%m-%d')
        print(skai.document.published_date.strftime('%Y-%m-%d'))

        return render(request, 'document/skai_edit.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        
        skai = DocSKAI.objects.get(pk=request.POST["pk"])
        doc = skai.document

        skai.year = request.POST["year"]
        doc.document_number = request.POST["document_number"]
        doc.regarding = request.POST["regarding"]
        doc.published_date = request.POST["published_date"]
        doc.save()
        skai.document = doc
        skai.save()

        if "file" in request.FILES:
            doc.file = request.FILES["file"]
            doc.save()
            skai.document = doc
            skai.save()
        
        #Macro doc later

        return redirect('document:doc-list-skai')

class LKAIListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year

        today = timezone.now()
        doc_skai = DocSKAI.objects.select_related('document').filter(document__published_date__year=today.year)
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        return render(request, 'document/lkai_list.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.select_related('document').filter(document__published_date__year=request.POST["year"])
        context["doc_skai"] = sorted(chain(doc_skai), key=lambda x: x.document.published_date, reverse=False)

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year
        return render(request, 'document/lkai_list.html', context)

class LKAIView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        context["skai"] = DocSKAI.objects.get(pk=pk)

        return render(request, 'document/lkai_view.html', context)

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

