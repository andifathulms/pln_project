from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from document.models import DocSKAI, MacroData

from openpyxl import load_workbook

from .models import LRPA_Monitoring, LRPA_File
from monev.models import PRK_Lookup, Assigned_PRK
from .forms import LRPAFileForm

class MonevView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        ### TRY TO AUTOMATE LATER ###
        # doc = DocSKAI.objects.filter(year=2022, lrpa_include=True).order_by('document__published_date')
        # first_macro_file = doc[0].macro.macro_file_1
        # first_macro_data = MacroData.objects.filter(macro_file=first_macro_file).order_by('no_prk')
        ### TRY TO AUTOMATE LATER ###
        

        #skai_1 = DocSKAI.objects.get(pk=8) #DEV
        skai_1 = DocSKAI.objects.get(pk=1) #PROD
        macro_1 = skai_1.macro.macro_file_1
        macro_data_1 = MacroData.objects.filter(macro_file=macro_1).order_by('no_prk')

        #skai_3 = DocSKAI.objects.get(pk=10) #DEV
        skai_3 = DocSKAI.objects.get(pk=3) #PROD
        macro_3 = skai_3.macro.macro_file_1
        #macro_data_3 = MacroData.objects.filter(macro_file=macro_3)

        #skai_2 = DocSKAI.objects.get(pk=19) #DEV
        skai_2 = DocSKAI.objects.get(pk=6) #PROD

        file_lookup = Assigned_PRK.objects.get(pk=1)
        #lookup = PRK_Lookup.objects.get(file=file_lookup)

        macro_2 = skai_2.macro.macro_file_1
        macro_data_2 = MacroData.objects.filter(macro_file=macro_2)


        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()

        list_1 = list(data.no_prk for data in macro_data_1)
        list_2 = list(data.no_prk for data in macro_data_2)

        #MANUAL!!!
        document = [skai_1, skai_2, last_lrpa, skai_3]
        context["document"] = document

        #MANUAL!!!
        residue_1 = list(set(list_1)-set(list_2))
        residue_2 = list(set(list_2)-set(list_1))

        combine_list = []
        
        for data in macro_data_1:
            try:
                temp = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_2)
                temp_2 = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_3)
                lrpa = LRPA_Monitoring.objects.get(no_prk=data.no_prk, file=last_lrpa)

                #get prk kode
                lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk).first() #return None if there isnt any
                
                #get total realisasi
                total_realisasi = int(lrpa.jan_realisasi_disburse) + int(lrpa.feb_realisasi_disburse) + int(lrpa.mar_realisasi_disburse) + int(lrpa.apr_realisasi_disburse) + int(lrpa.mei_realisasi_disburse) + int(lrpa.jun_realisasi_disburse) + int(lrpa.jul_realisasi_disburse) + int(lrpa.aug_realisasi_disburse) + int(lrpa.sep_realisasi_disburse) + int(lrpa.okt_realisasi_disburse) + int(lrpa.nov_realisasi_disburse) + int(lrpa.des_realisasi_disburse)
                if lrpa.real_aki():
                    sisa_aki = lrpa.real_aki() - total_realisasi
                else:
                    sisa_aki = 0
                
                if temp.no_prk != None:
                    combine_list.append((data,temp,lrpa,total_realisasi,sisa_aki,temp_2, lookup_prk))

                #print(data.macro_file.pk == temp.macro_file.pk)
            except Exception as e:
                #print("Skip " + str(data.no_prk))
                print(e)
        
        if len(residue_2) != 0:
            for prk in residue_2:
                try:
                    temp = MacroData.objects.get(no_prk=prk, macro_file=macro_2)
                    temp_2 = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_3)
                    lrpa = LRPA_Monitoring.objects.get(no_prk=prk, file=last_lrpa)

                    #get prk kode
                    lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk).first() #return None if there isnt any

                    #get total realisasi
                    total_realisasi = int(lrpa.jan_realisasi_disburse) + int(lrpa.feb_realisasi_disburse) + int(lrpa.mar_realisasi_disburse) + int(lrpa.apr_realisasi_disburse) + int(lrpa.mei_realisasi_disburse) + int(lrpa.jun_realisasi_disburse) + int(lrpa.jul_realisasi_disburse) + int(lrpa.aug_realisasi_disburse) + int(lrpa.sep_realisasi_disburse) + int(lrpa.okt_realisasi_disburse) + int(lrpa.nov_realisasi_disburse) + int(lrpa.des_realisasi_disburse)
                    
                    if lrpa.real_aki():
                        sisa_aki = lrpa.real_aki() - total_realisasi
                    else:
                        sisa_aki = 0
                    if temp.no_prk != None:
                        combine_list.append((None,temp,lrpa,total_realisasi,sisa_aki,temp_2,lookup_prk))
                except Exception as e:
                    print(e)
        
        context["data"] = combine_list
        
        return render(request, 'monev/monev_lkai.html', context)

class UploadLRPA(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        context = {}

        return render(request, 'monev/upload_lrpa.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        print(request.FILES)
        file = request.FILES["lrpa_file"]
        
        wb = load_workbook(file)
        ws = wb['Monitoring LRPA']

        start_col = 1
        end_col = 42

        list_rows = [idx for idx,cell in enumerate(ws["B"]) if cell.value and idx >= 6]
        #print(list_rows)
        
        doc_form = LRPAFileForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.upload_by = request.user
            doc.save()
            
            for rows in list_rows:
                row = [cell.value for cell in ws[rows][start_col:end_col+1]]
                try:
                    lrpa = LRPA_Monitoring(
                        file = doc,
                        no_prk = row[0],
                        disburse_year_before = row[9],
                        jan_rencana_disburse = row[18],
                        jan_realisasi_disburse = row[19],
                        feb_rencana_disburse = row[20],
                        feb_realisasi_disburse = row[21],
                        mar_rencana_disburse = row[22],
                        mar_realisasi_disburse = row[23],
                        apr_rencana_disburse = row[24],
                        apr_realisasi_disburse = row[25],
                        mei_rencana_disburse = row[26],
                        mei_realisasi_disburse = row[27],
                        jun_rencana_disburse = row[28],
                        jun_realisasi_disburse = row[29],
                        jul_rencana_disburse = row[30],
                        jul_realisasi_disburse = row[31],
                        aug_rencana_disburse = row[32],
                        aug_realisasi_disburse = row[33],
                        sep_rencana_disburse = row[34],
                        sep_realisasi_disburse = row[35],
                        okt_rencana_disburse = row[36],
                        okt_realisasi_disburse = row[37],
                        nov_rencana_disburse = row[38],
                        nov_realisasi_disburse = row[39],
                        des_rencana_disburse = row[40],
                        des_realisasi_disburse = row[41],
                        mekanisme_pembayaran = row[14],
                        ai_this_year = row[10],
                        aki_this_year = row[11]
                    )

                    lrpa.save()
                except Exception as e:
                    print(e)
        else:
            print(doc_form.errors)

        return render(request, 'monev/upload_lrpa.html', context)

class LRPAList(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}

        lrpa = LRPA_File.objects.all()
        context["lrpa"] = lrpa

        return render(request, 'monev/list_lrpa.html', context)