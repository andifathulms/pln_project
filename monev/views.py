from cmath import log
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from document.models import DocSKAI, MacroData

from openpyxl import load_workbook

from .models import LRPA_Monitoring, LRPA_File
from monev.models import PRK_Lookup, Assigned_PRK
from .forms import LRPAFileForm

def safe_div(x,y):
    if y==0: return 0
    return x/y

class MonevView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        file_lookup = Assigned_PRK.objects.get(pk=1) #MANUAL


        #COUNT FOR "REN"
        ren_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="REN")
        
        sum_ai_ren = 0
        sum_aki_ren = 0
        ren_realisasi = 0
        for prk in ren_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_ren = sum_ai_ren + lrpa.real_ai()
            sum_aki_ren = sum_aki_ren + lrpa.real_aki()
            ren_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            ren_realisasi = ren_realisasi + ren_realisasi_temp

        ren_sisa = sum_aki_ren-ren_realisasi
        ren_pct = (ren_realisasi/sum_aki_ren)*100

        context["ren_ai"] = sum_ai_ren
        context["ren_aki"] = sum_aki_ren
        context["ren_realisasi"] = ren_realisasi
        context["ren_sisa"] = ren_sisa
        context["ren_pct"] = ren_pct
        #END COUNT FOR "REN"

        #COUNT FOR "PPK"
        ppk_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="PPK")
        
        sum_ai_ppk = 0
        sum_aki_ppk = 0
        ppk_realisasi = 0
        for prk in ppk_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_ppk = sum_ai_ppk + lrpa.real_ai()
            sum_aki_ppk = sum_aki_ppk + lrpa.real_aki()
            ppk_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            ppk_realisasi = ppk_realisasi + ppk_realisasi_temp

        ppk_sisa = sum_aki_ppk-ppk_realisasi
        ppk_pct = (ppk_realisasi/sum_aki_ppk)*100

        context["ppk_ai"] = sum_ai_ppk
        context["ppk_aki"] = sum_aki_ppk
        context["ppk_realisasi"] = ppk_realisasi
        context["ppk_sisa"] = ppk_sisa
        context["ppk_pct"] = ppk_pct
        #END COUNT FOR "PPK"

        #COUNT FOR "OPK 1"
        opk1_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="OPK 1")
        
        sum_ai_opk1 = 0
        sum_aki_opk1 = 0
        opk1_realisasi = 0
        for prk in opk1_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_opk1 = sum_ai_opk1 + lrpa.real_ai()
            sum_aki_opk1 = sum_aki_opk1 + lrpa.real_aki()
            opk1_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            opk1_realisasi = opk1_realisasi + opk1_realisasi_temp

        opk1_sisa = sum_aki_opk1-opk1_realisasi
        opk1_pct = (opk1_realisasi/sum_aki_opk1)*100

        context["opk1_ai"] = sum_ai_opk1
        context["opk1_aki"] = sum_aki_opk1
        context["opk1_realisasi"] = opk1_realisasi
        context["opk1_sisa"] = opk1_sisa
        context["opk1_pct"] = opk1_pct
        #END COUNT FOR "OPK 1"

        #COUNT FOR "OPK 2"
        opk2_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="OPK 2")
        
        sum_ai_opk2 = 0
        sum_aki_opk2 = 0
        opk2_realisasi = 0
        for prk in opk2_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_opk2 = sum_ai_opk2 + lrpa.real_ai()
            sum_aki_opk2 = sum_aki_opk2 + lrpa.real_aki()
            opk2_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            opk2_realisasi = opk2_realisasi + opk2_realisasi_temp

        opk2_sisa = sum_aki_opk2-opk2_realisasi
        opk2_pct = (opk2_realisasi/sum_aki_opk2)*100

        context["opk2_ai"] = sum_ai_opk2
        context["opk2_aki"] = sum_aki_opk2
        context["opk2_realisasi"] = opk2_realisasi
        context["opk2_sisa"] = opk2_sisa
        context["opk2_pct"] = opk2_pct
        #END COUNT FOR "OPK 2"

        #COUNT FOR "K3L"
        k3l_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="K3L")
        
        sum_ai_k3l = 0
        sum_aki_k3l = 0
        k3l_realisasi = 0
        for prk in k3l_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_k3l = sum_ai_k3l + lrpa.real_ai()
            sum_aki_k3l = sum_aki_k3l + lrpa.real_aki()
            k3l_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            k3l_realisasi = k3l_realisasi + k3l_realisasi_temp

        k3l_sisa = sum_aki_k3l-k3l_realisasi
        k3l_pct = (k3l_realisasi/sum_aki_k3l)*100

        context["k3l_ai"] = sum_ai_k3l
        context["k3l_aki"] = sum_aki_k3l
        context["k3l_realisasi"] = k3l_realisasi
        context["k3l_sisa"] = k3l_sisa
        context["k3l_pct"] = k3l_pct
        #END COUNT FOR "K3L"

        #COUNT FOR "UPP 1"
        upp1_prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo="UPP") #CHANGE LATER
        
        sum_ai_upp1 = 0
        sum_aki_upp1 = 0
        upp1_realisasi = 0
        for prk in upp1_prk:
            lrpa = LRPA_Monitoring.objects.get(no_prk=prk.no_prk, file=last_lrpa)
            sum_ai_upp1 = sum_ai_upp1 + lrpa.real_ai()
            sum_aki_upp1 = sum_aki_upp1 + lrpa.real_aki()
            upp1_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
            upp1_realisasi = upp1_realisasi + upp1_realisasi_temp

        upp1_sisa = sum_aki_upp1-upp1_realisasi
        upp1_pct = (upp1_realisasi/sum_aki_upp1)*100

        context["upp1_ai"] = sum_ai_upp1
        context["upp1_aki"] = sum_aki_upp1
        context["upp1_realisasi"] = upp1_realisasi
        context["upp1_sisa"] = upp1_sisa
        context["upp1_pct"] = upp1_pct
        #END COUNT FOR "UPP 1"

        #COUNT FOR ALL PRK IN "Pekerjaan. Prasarana"
        A_PRK_1 = ["Survey dan Soil Investigasi", "Perijinan", "Studi Lingkungan/AMDAL/UKL-UPL/LARAP", "Jasa Konsultasi Pembebasan tanah & ROW", "Inventarisasi, Pembebasan tanah & ROW"]
        A_PRK_2 = ["SV", "IZ", "LH", "JP", "TN"]

        A_list = []

        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        for idx,x in enumerate(A_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                temp_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                temp_realisasi = temp_realisasi + temp_realisasi_temp
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (temp_realisasi/sum_aki_temp)*100

            A_list.append((A_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
        
        context["A_list"] = A_list
        #END COUNT FOR ALL PRK IN "Pekerjaan. Prasarana"

        #COUNT FOR ALL PRK IN "Pekerjaan. Utama"
        B_PRK_1 = ["Pembangunan KIT/TL/GI ", "Pengadaan KIT/TL/GI/Trafo", "Jasa konsultasi Enginering dan Konstruksi (KIT)", "Pemantauan & Pengelolaan Lingkungan Thp Kons", "Pengadaan Tower/Konduktor/MTU/HV/Trafo (TL dan GI)","Pek. Penyempurnaan KIT/Biaya Pra COD","Pek. Penyempurnaan TL dan GI"]
        B_PRK_2 = ["PB", "PD", "JS", "PL", "SWA","PP KIT","PP TL/GI"]

        B_list = []

        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        for idx,x in enumerate(B_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                temp_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                temp_realisasi = temp_realisasi + temp_realisasi_temp
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            B_list.append((B_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["B_list"] = B_list
        #END COUNT FOR ALL PRK IN "Pekerjaan. Utama"

        #COUNT FOR ALL PRK IN "Pekerjaan. Lainnya"
        C_PRK_1 = ["IPPKH", "Jasa Bantuan Hukum & Manajemen Stakholder", "Jasa terkait SLO/Kommisioning (KIT)", "Jasa terkait SLO/Kommisioning (TL dan GI)", "Jasa Konstruksi & QA/QC oleh PMK (KIT)","Jasa Konstruksi & QA/QC oleh PMK (TL dan GI)","Biaya Sertifikat","Jasa Penyusunan Bid Doc dan HPE"]
        C_PRK_2 = ["KH", "KUM", "SER KIT", "SER TL/GI", "PMK KIT","PMK TL/GI","BS","PLIS"]

        C_list = []

        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        for idx,x in enumerate(C_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                temp_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                temp_realisasi = temp_realisasi + temp_realisasi_temp
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            C_list.append((C_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["C_list"] = C_list
        #END COUNT FOR ALL PRK IN "Pekerjaan. Lainnya"

        return render(request, 'monev/monev_view.html', context)

class LKAIView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        ### TRY TO AUTOMATE LATER ###
        # doc = DocSKAI.objects.filter(year=2022, lrpa_include=True).order_by('document__published_date')
        # first_macro_file = doc[0].macro.macro_file_1
        # first_macro_data = MacroData.objects.filter(macro_file=first_macro_file).order_by('no_prk')
        ### TRY TO AUTOMATE LATER ###

        #GET USER DIVISION
        division = request.user.division
        

        skai_1 = DocSKAI.objects.get(pk=8) #DEV
        #skai_1 = DocSKAI.objects.get(pk=1) #PROD
        macro_1 = skai_1.macro.macro_file_1
        macro_data_1 = MacroData.objects.filter(macro_file=macro_1).order_by('no_prk')

        skai_3 = DocSKAI.objects.get(pk=10) #DEV
        #skai_3 = DocSKAI.objects.get(pk=3) #PROD
        macro_3 = skai_3.macro.macro_file_1
        #macro_data_3 = MacroData.objects.filter(macro_file=macro_3)

        skai_2 = DocSKAI.objects.get(pk=19) #DEV
        #skai_2 = DocSKAI.objects.get(pk=6) #PROD

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

        if division == "Super Admin" or division == "ANG":
            context["for_div"] = "ALL"
        else:
            context["for_div"] = division
        
        combine_list = []
        
        for data in macro_data_1:
            try:
                temp = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_2)
                temp_2 = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_3)
                lrpa = LRPA_Monitoring.objects.get(no_prk=data.no_prk, file=last_lrpa)

                #get total realisasi
                total_realisasi = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                if lrpa.real_aki():
                    sisa_aki = lrpa.real_aki() - total_realisasi
                else:
                    sisa_aki = 0
                
                # Get PRK kode lookup
                # Determine User View

                if division == "Super Admin" or division == "ANG":
                    lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk).first() #return None if there isnt any
                    if temp.no_prk != None:
                        combine_list.append((data,temp,lrpa,total_realisasi,sisa_aki,temp_2, lookup_prk))
                else:
                    lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk, rekap_user_induk=division).first()
                    if temp.no_prk != None and lookup_prk != None: #CHANGE THIS TO WORK!!
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
                    
                    # Get PRK kode lookup
                    # Determine User View

                    if division == "Super Admin" or division == "ANG":
                        lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk).first() #return None if there isnt any
                        if temp.no_prk != None:
                            combine_list.append((data,temp,lrpa,total_realisasi,sisa_aki,temp_2, lookup_prk))
                    else:
                        lookup_prk = PRK_Lookup.objects.filter(file=file_lookup, no_prk=data.no_prk, rekap_user_induk=division).first()
                        if temp.no_prk != None and lookup_prk != None: #CHANGE THIS TO WORK!!
                            combine_list.append((data,temp,lrpa,total_realisasi,sisa_aki,temp_2, lookup_prk))
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