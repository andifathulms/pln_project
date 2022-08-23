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

        #START COMPUTE FOR MONEV BY BPO
        #COUNT FOR BPO BESIDE "UPP"
        BPO_1 = ["Perencanaan", "Perizinan, Pertanahan, dan Komunikasi", "Operasi Konstruksi 1", "Operasi Konstruksi 2", "K3L"]
        BPO_2 = ["REN", "PPK", "OPK 1", "OPK 2", "K3L"]

        BPO_list = []

        total_ai_bpo = 0
        total_aki_bpo = 0
        total_realisasi_bpo = 0

        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        
        for idx,x in enumerate(BPO_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                temp_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                temp_realisasi = temp_realisasi + temp_realisasi_temp
            
            total_ai_bpo = total_ai_bpo + sum_ai_temp
            total_aki_bpo = total_aki_bpo + sum_aki_temp
            total_realisasi_bpo = total_realisasi_bpo + temp_realisasi

            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (temp_realisasi/sum_aki_temp)*100

            BPO_list.append((BPO_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
        
        #COUNT FOR BPO "UPP"
        BPO_UPP_1 = ["UPP KITRING SULSEL","UPP KITRING SULTENG","UPP KITRING SULTRA","UPP KITRING SULUT dan GORONTALO"]
        BPO_UPP_2 = ["UPP 1","UPP 2", "UPP 3", "UPP 4"]

        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        for idx,x in enumerate(BPO_UPP_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, upp=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                temp_realisasi_temp = int(lrpa.jan_realisasi_disburse or 0) + int(lrpa.feb_realisasi_disburse or 0) + int(lrpa.mar_realisasi_disburse or 0) + int(lrpa.apr_realisasi_disburse or 0) + int(lrpa.mei_realisasi_disburse or 0) + int(lrpa.jun_realisasi_disburse or 0) + int(lrpa.jul_realisasi_disburse or 0) + int(lrpa.aug_realisasi_disburse or 0) + int(lrpa.sep_realisasi_disburse or 0) + int(lrpa.okt_realisasi_disburse or 0) + int(lrpa.nov_realisasi_disburse or 0) + int(lrpa.des_realisasi_disburse or 0)
                temp_realisasi = temp_realisasi + temp_realisasi_temp
            
            total_ai_bpo = total_ai_bpo + sum_ai_temp
            total_aki_bpo = total_aki_bpo + sum_aki_temp
            total_realisasi_bpo = total_realisasi_bpo + temp_realisasi

            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            BPO_list.append((BPO_UPP_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
        
        context["BPO_list"] = BPO_list

        context["total_ai_bpo"] = total_ai_bpo
        context["total_aki_bpo"] = total_aki_bpo
        context["total_realisasi_bpo"] = total_realisasi_bpo
        context["total_sisa_aki_bpo"] = total_aki_bpo - total_realisasi_bpo
        context["total_pct_bpo"] = (safe_div(total_realisasi_bpo,total_aki_bpo))*100


        #START COMPUTE FOR MONEV BY PRK
        #COUNT FOR ALL PRK IN "Pekerjaan. Prasarana"
        A_PRK_1 = ["Survey dan Soil Investigasi", "Perijinan", "Studi Lingkungan/AMDAL/UKL-UPL/LARAP", "Jasa Konsultasi Pembebasan tanah & ROW", "Inventarisasi, Pembebasan tanah & ROW"]
        A_PRK_2 = ["SV", "IZ", "LH", "JP", "TN"]

        A_list = []

        total_ai_a = 0
        total_aki_a = 0
        total_realisasi_a = 0

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
            
            total_ai_a = total_ai_a + sum_ai_temp
            total_aki_a = total_aki_a + sum_aki_temp
            total_realisasi_a = total_realisasi_a + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (temp_realisasi/sum_aki_temp)*100

            A_list.append((A_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
        
        context["A_list"] = A_list

        context["total_ai_a"] = total_ai_a
        context["total_aki_a"] = total_aki_a
        context["total_realisasi_a"] = total_realisasi_a
        context["total_sisa_aki_a"] = total_aki_a - total_realisasi_a
        context["total_pct_a"] = (safe_div(total_realisasi_a,total_aki_a))*100
        #END COUNT FOR ALL PRK IN "Pekerjaan. Prasarana"

        #COUNT FOR ALL PRK IN "Pekerjaan. Utama"
        B_PRK_1 = ["Pembangunan KIT/TL/GI ", "Pengadaan KIT/TL/GI/Trafo", "Jasa konsultasi Enginering dan Konstruksi (KIT)", "Pemantauan & Pengelolaan Lingkungan Thp Kons", "Pengadaan Tower/Konduktor/MTU/HV/Trafo (TL dan GI)","Pek. Penyempurnaan KIT/Biaya Pra COD","Pek. Penyempurnaan TL dan GI"]
        B_PRK_2 = ["PB", "PD", "JS", "PL", "SWA","PP KIT","PP TL/GI"]

        B_list = []

        total_ai_b = 0
        total_aki_b = 0
        total_realisasi_b = 0

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
            
            total_ai_b = total_ai_b + sum_ai_temp
            total_aki_b = total_aki_b + sum_aki_temp
            total_realisasi_b = total_realisasi_b + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            B_list.append((B_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["B_list"] = B_list

        context["total_ai_b"] = total_ai_b
        context["total_aki_b"] = total_aki_b
        context["total_realisasi_b"] = total_realisasi_b
        context["total_sisa_aki_b"] = total_aki_b - total_realisasi_b
        context["total_pct_b"] = (safe_div(total_realisasi_b,total_aki_b))*100
        #END COUNT FOR ALL PRK IN "Pekerjaan. Utama"

        #COUNT FOR ALL PRK IN "Pekerjaan. Lainnya"
        C_PRK_1 = ["IPPKH", "Jasa Bantuan Hukum & Manajemen Stakholder", "Jasa terkait SLO/Kommisioning (KIT)", "Jasa terkait SLO/Kommisioning (TL dan GI)", "Jasa Konstruksi & QA/QC oleh PMK (KIT)","Jasa Konstruksi & QA/QC oleh PMK (TL dan GI)","Biaya Sertifikat","Jasa Penyusunan Bid Doc dan HPE"]
        C_PRK_2 = ["KH", "KUM", "SER KIT", "SER TL/GI", "PMK KIT","PMK TL/GI","BS","PLIS"]

        C_list = []

        total_ai_c = 0
        total_aki_c = 0
        total_realisasi_c = 0

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
            
            total_ai_c = total_ai_c + sum_ai_temp
            total_aki_c = total_aki_c + sum_aki_temp
            total_realisasi_c = total_realisasi_c + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            C_list.append((C_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["C_list"] = C_list

        context["total_ai_c"] = total_ai_c
        context["total_aki_c"] = total_aki_c
        context["total_realisasi_c"] = total_realisasi_c
        context["total_sisa_aki_c"] = total_aki_c - total_realisasi_c
        context["total_pct_c"] = (safe_div(total_realisasi_c,total_aki_c))*100

        total_ai_prk = total_ai_a + total_ai_b + total_ai_c
        total_aki_prk = total_aki_a + total_aki_b + total_aki_c
        total_realisasi_prk = total_realisasi_a + total_realisasi_b + total_realisasi_c
        total_sisa_aki_prk = total_aki_prk - total_realisasi_prk

        context["total_ai_prk"] = total_ai_prk
        context["total_aki_prk"] = total_aki_prk
        context["total_realisasi_prk"] = total_realisasi_prk
        context["total_sisa_aki_prk"] = total_sisa_aki_prk
        context["total_pct_prk"] = (safe_div(total_realisasi_prk,total_aki_prk))*100
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