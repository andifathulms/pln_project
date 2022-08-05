from urllib import request
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect

from .models import Document, DocSKAI, MacroFile, Macro, MacroData
from .forms import DocumentForm

from itertools import chain

from tablib import Dataset
from django.utils import timezone

from openpyxl import load_workbook

class SKAIListView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        today = timezone.now()
        doc_skai_1 = DocSKAI.objects.select_related('document').filter(document__published_date__year=today.year, type="Penetapan")
        doc_skai_2 = DocSKAI.objects.select_related('document').filter(document__published_date__year=today.year, type="Usulan")

        context["doc_skai_1"] = sorted(chain(doc_skai_1), key=lambda x: x.document.published_date, reverse=False)
        context["doc_skai_2"] = sorted(chain(doc_skai_2), key=lambda x: x.document.published_date, reverse=False)
        context["doc_skai_3"] = sorted(chain(doc_skai_1, doc_skai_2), key=lambda x: x.document.published_date, reverse=False)

        if pk == 1:
            context["doc_skai"] = sorted(chain(doc_skai_1), key=lambda x: x.document.published_date, reverse=False)
            context["skai_verb"] = "Penetapan"
        elif pk == 2:
            context["doc_skai"] = sorted(chain(doc_skai_2), key=lambda x: x.document.published_date, reverse=False)
            context["skai_verb"] = "Usulan"
        elif pk == 3:
            context["doc_skai"] = sorted(chain(doc_skai_1, doc_skai_2), key=lambda x: x.document.published_date, reverse=False)
            context["skai_verb"] = ""
        else:
            return HttpResponseRedirect(reverse('not_found'))

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year

        context['the_year'] = today.year
        return render(request, 'document/list_skai.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        doc_skai_1 = DocSKAI.objects.select_related('document').filter(document__published_date__year=request.POST["year"], type="Penetapan")
        doc_skai_2 = DocSKAI.objects.select_related('document').filter(document__published_date__year=request.POST["year"], type="Usulan")
        
        context["doc_skai_1"] = sorted(chain(doc_skai_1), key=lambda x: x.document.published_date, reverse=False)
        context["doc_skai_2"] = sorted(chain(doc_skai_2), key=lambda x: x.document.published_date, reverse=False)
        context["doc_skai_3"] = sorted(chain(doc_skai_1, doc_skai_2), key=lambda x: x.document.published_date, reverse=False)

        year = DocSKAI.objects.values("year").distinct()
        context['year'] = year
        context['the_year'] = request.POST["year"]
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

                skai = DocSKAI(document=doc, year=request.POST['year'],keyword=request.POST['keyword'],revision=False,macro_doc=request.FILES["file_xls"])
                skai.save()

                #skai.create_notif_on_upload(skai.document.uploader,skai.document.regarding)
            else:
                print(doc.errors)
        elif 'submit-skai-usulan' in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI(document=doc, year=request.POST['year'],keyword=request.POST['keyword'],type="Usulan",macro_doc=request.FILES["file_xls"])
                skai.save()
                #skai.create_notif_on_upload(skai.document.uploader,skai.document.regarding)
        
        doc_skai = DocSKAI.objects.all()
        context["doc_skai"] = list(chain(doc_skai))

        return render(request, 'document/upload_SKAI.html', context)

class XLSM_Playground(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}

        # doc = DocSKAI.objects.get(pk=18)
        # context["macros"] = doc.macro_doc

        # print("Load Workbook")
        # wb = load_workbook(doc.macro_doc, keep_vba=True, data_only=True)
        # print("Done")
        # ws = wb['LKAI IDR']

        # start_col = 2
        # end_col = 24

        # list_rows = [idx for idx,cell in enumerate(ws["c"]) if cell.value and idx >= 9]

        # for rows in list_rows:
        #     if ws["C"][rows].value != None:
                
        #         print("Row = " + str(rows))
        #         row = [cell.value for cell in ws[rows][start_col:end_col+1]]
        #         print(row)
            
        #     else:
        #         print("continue : " + str(rows))
        #         continue
        
        # print("Done!!!")

        return render(request, 'document/playground.html', context)

