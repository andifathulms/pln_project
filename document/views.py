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
        skai.keyword = request.POST["keyword"]

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

        return redirect('home')


class LKAIView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        skai = DocSKAI.objects.get(pk=pk)
        macro = skai.macro
        macro_1 = macro.macro_file_1

        macro_data = MacroData.objects.filter(macro_file=macro_1)

        context["skai"] = skai
        context["macros"] = macro_data

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

class XLSM_Playground(UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.is_admin

    def get(self, request, *args, **kwargs):
        context = {}

        doc = DocSKAI.objects.get(pk=1)
        context["macros"] = doc.macro_doc

        print("Load Workbook")
        wb = load_workbook(doc.macro_doc, keep_vba=True, data_only=True)
        print("Done")
        print(wb.sheetnames)
        ws = wb['LKAI IDR']
        ws_2 = wb['LKAI IDR 2']

        start_col = 31
        end_col = 58

        start_col_2 = 1
        end_col_2 = 40

        list_rows = [idx for idx,cell in enumerate(ws["AF"]) if cell.value and idx >= 9]
        print(list_rows)
        print(ws['C'][9].value)
        macro_file = MacroFile()
        macro_file.save()

        for rows in list_rows:
            if ws["AF"][rows].value != None:
                
                print("Row = " + str(rows))
                row = [cell.value for cell in ws[rows][start_col:end_col+1]]
                row_2 = [cell.value for cell in ws_2[rows][start_col_2:end_col_2+1]]
                print(row)
                print(row_2)

                try:
                    macro_data = MacroData(macro_file = macro_file,
                        no_prk = row[0],
                        no_program = row[1],
                        no_ruptl = row[2],
                        cluster = row[3],
                        fungsi = row[4],
                        sub_fungsi = row[5],
                        program_utama = row[6],
                        score = row[7],
                        jenis_program = row[8],
                        keg_no = row[9],
                        keg_uraian = row[10],
                        keg_target_fisik = row[11],
                        keg_satuan = row[12],
                        ang_nilai = row[13],
                        ang_status = row[14],
                        ang_jenis_kontrak = row[15],
                        ang_no_kontrak = row[16],
                        realisasi_pembayaran = row[17],
                        prediksi_pembayaran = row[18],
                        ai_this_year = row[19],
                        aki_this_year = row[20],
                        aki_n1_year = row[21],
                        aki_n2_year = row[22],
                        aki_n3_year = row[23],
                        aki_n4_year = row[24],
                        aki_after_n1_year = row[25],
                        sumber_dana = row[26],
                        rencana_terkontrak = row_2[14],
                        rencana_COD = row_2[15],
                        jan_progress_fisik   = row_2[16],
                        jan_rencana_disburse = row_2[17], 
                        feb_progress_fisik   = row_2[18], 
                        feb_rencana_disburse = row_2[19], 
                        mar_progress_fisik   = row_2[20], 
                        mar_rencana_disburse = row_2[21], 
                        apr_progress_fisik   = row_2[22], 
                        apr_rencana_disburse = row_2[23], 
                        mei_progress_fisik   = row_2[24], 
                        mei_rencana_disburse = row_2[25], 
                        jun_progress_fisik   = row_2[26], 
                        jun_rencana_disburse = row_2[27], 
                        jul_progress_fisik   = row_2[28], 
                        jul_rencana_disburse = row_2[29], 
                        aug_progress_fisik   = row_2[30], 
                        aug_rencana_disburse = row_2[31], 
                        sep_progress_fisik   = row_2[32], 
                        sep_rencana_disburse = row_2[33], 
                        okt_progress_fisik   = row_2[34], 
                        okt_rencana_disburse = row_2[35], 
                        nov_progress_fisik   = row_2[36], 
                        nov_rencana_disburse = row_2[37], 
                        des_progress_fisik   = row_2[38], 
                        des_rencana_disburse = row_2[39] 
                    )
                    macro_data.save()

                except Exception as e:
                    print(e)                
            
            else:
                print("continue : " + str(rows))
                continue
        
        macro = Macro(macro_file_1=macro_file)
        macro.save()

        print("Done!!!")

        return render(request, 'document/playground.html', context)

