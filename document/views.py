from urllib import response
from django.http import HttpResponse, FileResponse, HttpResponseNotFound
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

class MacroView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        skai = DocSKAI.objects.get(pk=pk)
        context["macros"] = skai.macro.macro_file_1
        print(skai.macro.macro_file_1)

        return render(request, 'document/macro_view.html', context)

    def post(self, request, *args, **kwargs):
        pass

class SKAIComparison(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'document/skai_comparison.html', context)


class UploadSKAI(LoginRequiredMixin, View):
    
    #doc_skai = DocSKAI.objects.all()

    def get(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        context["skai_only"] = doc_skai
        context["doc_skai"] = list(chain(doc_skai))
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

class UploadLKAI(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        context["skai_only"] = doc_skai

        skai_with_macro = DocSKAI.objects.exclude(macro__isnull=True)
        context["skai_with_macro"] = skai_with_macro

        return render(request, 'document/upload_LKAI.html', context)

    
    def post(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        context["skai_only"] = doc_skai

        if 'submit-idr1' in request.POST:
            skai = DocSKAI.objects.get(pk=request.POST["skai"])

            files_1 = request.FILES["file_1"]
            dataset_1 = Dataset()
            imported_data_1 = dataset_1.load(files_1.read(), format='xlsx')

            macro = Macro()

            macro_file_1 = MacroFile(uploader=request.user)
            macro_file_1.save()

            for data in imported_data_1:
                macro_data_1 = MacroData(
                    macro_file=macro_file_1,
                    no_prk=data[0],no_program=data[1],no_ruptl=data[2],
                    cluster=data[3],fungsi=data[4],sub_fungsi=data[5],
                    program_utama=data[6],score=data[7],jenis_program=data[8],
                    keg_no=data[9],keg_uraian=data[10],keg_target_fisik=data[11],
                    keg_satuan=data[12],ang_nilai=data[13],ang_status=data[14],
                    ang_jenis_kontrak=data[15],ang_no_kontrak=data[16],realisasi_pembayaran=data[17],
                    prediksi_pembayaran=data[18],ai_this_year=data[19],aki_this_year=data[20],
                    aki_n1_year=data[21],aki_n2_year=data[22],aki_n3_year=data[23],
                    aki_n4_year=data[24],aki_after_n1_year=data[25],sumber_dana=data[26]
                )
                macro_data_1.save()

            macro.macro_file_1 = macro_file_1
            macro.save()
            
            try:
                files_2 = request.FILES["file_2"]
                dataset_2 = Dataset()
                imported_data_2 = dataset_2.load(files_2.read(), format='xlsx')

                macro_file_2 = MacroFile(uploader=request.user)
                macro_file_2.save()
                
                for data in imported_data_2:
                    macro_data_2 = MacroData(
                        macro_file=macro_file_2,
                        no_prk=data[0],no_program=data[1],no_ruptl=data[2],
                        cluster=data[3],fungsi=data[4],sub_fungsi=data[5],
                        program_utama=data[6],score=data[7],jenis_program=data[8],
                        keg_no=data[9],keg_uraian=data[10],keg_target_fisik=data[11],
                        keg_satuan=data[12],ang_nilai=data[13],ang_status=data[14],
                        ang_jenis_kontrak=data[15],ang_no_kontrak=data[16],realisasi_pembayaran=data[17],
                        prediksi_pembayaran=data[18],ai_this_year=data[19],aki_this_year=data[20],
                        aki_n1_year=data[21],aki_n2_year=data[22],aki_n3_year=data[23],
                        aki_n4_year=data[24],aki_after_n1_year=data[25],sumber_dana=data[26]
                    )
                    macro_data_2.save()
                
                macro.macro_file_2 = macro_file_2
                macro.save()
            except:
                pass
        
            skai.macro = macro
            skai.save()

        return render(request, 'document/upload_LKAI.html', context)



def pdfViewer(request, pk):
    context = {}
    document = Document.objects.get(pk=pk)
    context["url"] = document.file.url

    response = render(request, 'pdfjs.html', context)
    
    response['Content-Disposition'] = 'inline;'
    response['Content-Type'] = 'application/pdf;'

    print(response.headers)
    return response
