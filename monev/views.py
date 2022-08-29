from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from django.db import models
from django.db.models import Sum, OuterRef, Subquery, F, Value
from django.db.models.functions import Round

from document.models import DocSKAI, MacroData

from openpyxl import load_workbook

from .models import LRPA_Monitoring, LRPA_File, PRK_Lookup, Assigned_PRK, MouPengalihanData, FileMouPengalihan
from .forms import LRPAFileForm, MouFileForm

from datetime import datetime
import sys

def safe_div(x,y):
    if y==0: return 0
    return x/y

def this_month():
    return datetime.now().month

def is_production():
    return False

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}

        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        last_mou = FileMouPengalihan.objects.order_by('file_export_date').first()
        file_lookup = Assigned_PRK.objects.get(pk=1) #MANUAL

        pembayaran = ["Unit", "Pusat", "Pengalihan"]
        data_1 = []
        for idx,x in enumerate(pembayaran):
            sum_ai = int(LRPA_Monitoring.objects.filter(file=last_lrpa,mekanisme_pembayaran=x).aggregate(Sum('ai_this_year'))['ai_this_year__sum'])
            sum_aki = int(LRPA_Monitoring.objects.filter(file=last_lrpa,mekanisme_pembayaran=x).aggregate(Sum('aki_this_year'))['aki_this_year__sum'])
            sum_realisasi = int(sum([m.sum_realisasi() for m in LRPA_Monitoring.objects.filter(file=last_lrpa,mekanisme_pembayaran=x)]))
            pct = (sum_realisasi*100)/sum_aki
            sisa = sum_aki - sum_realisasi
            
            data_1.append((pembayaran[idx],sum_ai,sum_aki,sum_realisasi,pct,sisa))

        context["data_1"] = data_1
        
        bpo = ["REN", "PPK", "OPK 1", "OPK 2", "K3L"]
        data_2 = []
        for idx,x in enumerate(bpo):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo=x).values_list('no_prk')
            prk_1 = LRPA_Monitoring.objects.filter(file=last_lrpa,mekanisme_pembayaran="Pengalihan").values_list('no_prk')
            prk_list = [p[0] for p in prk]
            prk_list_1 = [p[0] for p in prk_1]

            not_union = [p for p in prk_list if p not in prk_list_1]
            union = list(set(prk_list).intersection(prk_list_1)) # intersection between pengalihan and bpo
            
            #ADD IF PENGALIHAN
            sum_of_akb = int(sum([p.get_rencana_bulan(this_month()) for p in LRPA_Monitoring.objects.filter(no_prk__in=prk_list,file=last_lrpa)]))
            sum_of_realisasi_0 = int(sum([p.get_realisasi_bulan(this_month()) for p in LRPA_Monitoring.objects.filter(no_prk__in=not_union,file=last_lrpa)]))
            mou = MouPengalihanData.objects.filter(no_prk__in=union,file=last_mou)
            #print(x)
            #for p in mou: print(p.get_realisasi_bulan(this_month()),x)
            sum_of_realisasi_1 = int(sum([p.get_realisasi_bulan(this_month()) if p else 0 for p in mou]))
            sum_of_realisasi = sum_of_realisasi_0 + sum_of_realisasi_1
            sisa = sum_of_akb - sum_of_realisasi
            try:
                pct = (sisa*100)/sum_of_akb
            except:
                pct = 0
            data_2.append((x, sum_of_akb, sum_of_realisasi,sisa,pct))

        
        context["data_2"] = data_2
        return render(request, 'account/dashboard.html', context)

class MonevView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["month"] = this_month()
        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        last_mou = FileMouPengalihan.objects.order_by('file_export_date').first()
        file_lookup = Assigned_PRK.objects.get(pk=1) #MANUAL

        month = this_month() #CHANGE LATER TO LAST MOU MONTH

        #START COMPUTE FOR MONEV BY BPO
        #COUNT FOR BPO BESIDE "UPP"
        BPO_1 = ["Perencanaan", "Perizinan, Pertanahan, dan Komunikasi", "Operasi Konstruksi 1", "Operasi Konstruksi 2", "K3L"]
        BPO_2 = ["REN", "PPK", "OPK 1", "OPK 2", "K3L"]

        BPO_list = []

        total_ai_bpo = 0
        total_aki_bpo = 0
        total_realisasi_bpo = 0

        count_bpo = 0
        count_bpo_total = 0
        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        
        for idx,x in enumerate(BPO_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_bpo=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                lrpa_realisasi = [int(lrpa.jan_realisasi_disburse or 0), int(lrpa.feb_realisasi_disburse or 0), int(lrpa.mar_realisasi_disburse or 0), int(lrpa.apr_realisasi_disburse or 0), int(lrpa.mei_realisasi_disburse or 0), int(lrpa.jun_realisasi_disburse or 0), int(lrpa.jul_realisasi_disburse or 0), int(lrpa.aug_realisasi_disburse or 0), int(lrpa.sep_realisasi_disburse or 0), int(lrpa.okt_realisasi_disburse or 0), int(lrpa.nov_realisasi_disburse or 0), int(lrpa.des_realisasi_disburse or 0)]
                try:
                    mou = MouPengalihanData.objects.get(no_prk=p.no_prk, file=last_mou)
                    mou_realisasi = [int(mou.jan or 0), int(mou.feb or 0), int(mou.mar or 0), int(mou.apr or 0), int(mou.mei or 0), int(mou.jun or 0), int(mou.jul or 0), int(mou.aug or 0), int(mou.sep or 0), int(mou.okt or 0), int(mou.nov or 0), int(mou.des or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print(sum(lrpa_realisasi), " - ", lrpa_realisasi[month-1], " + ", mou_realisasi[month+1])
                except ValueError:
                    mou_realisasi = [int(float(mou.jan) or 0), int(float(mou.feb) or 0), int(float(mou.mar) or 0), int(float(mou.apr) or 0), int(float(mou.mei) or 0), int(float(mou.jun) or 0), int(float(mou.jul) or 0), int(float(mou.aug) or 0), int(float(mou.sep) or 0), int(float(mou.okt) or 0), int(float(mou.nov) or 0), int(float(mou.des) or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print("FLOAT")
                except MouPengalihanData.DoesNotExist:
                    temp_realisasi_temp = sum(lrpa_realisasi)
                
                temp_realisasi = temp_realisasi + temp_realisasi_temp
                count_bpo = count_bpo + 1
            
            count_bpo_total = count_bpo_total + count_bpo

            total_ai_bpo = total_ai_bpo + sum_ai_temp
            total_aki_bpo = total_aki_bpo + sum_aki_temp
            total_realisasi_bpo = total_realisasi_bpo + temp_realisasi

            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (temp_realisasi/sum_aki_temp)*100

            BPO_list.append((BPO_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct,count_bpo))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
            count_bpo = 0
        
        #COUNT FOR BPO "UPP"
        BPO_UPP_1 = ["UPP KITRING SULSEL","UPP KITRING SULTENG","UPP KITRING SULTRA","UPP KITRING SULUT dan GORONTALO"]
        BPO_UPP_2 = ["UPP 1","UPP 2", "UPP 3", "UPP 4"]

        count_bpo = 0
        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        for idx,x in enumerate(BPO_UPP_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, upp=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                lrpa_realisasi = [int(lrpa.jan_realisasi_disburse or 0), int(lrpa.feb_realisasi_disburse or 0), int(lrpa.mar_realisasi_disburse or 0), int(lrpa.apr_realisasi_disburse or 0), int(lrpa.mei_realisasi_disburse or 0), int(lrpa.jun_realisasi_disburse or 0), int(lrpa.jul_realisasi_disburse or 0), int(lrpa.aug_realisasi_disburse or 0), int(lrpa.sep_realisasi_disburse or 0), int(lrpa.okt_realisasi_disburse or 0), int(lrpa.nov_realisasi_disburse or 0), int(lrpa.des_realisasi_disburse or 0)]
                    
                try:
                    mou = MouPengalihanData.objects.get(no_prk=p.no_prk, file=last_mou)
                    mou_realisasi = [int(mou.jan or 0), int(mou.feb or 0), int(mou.mar or 0), int(mou.apr or 0), int(mou.mei or 0), int(mou.jun or 0), int(mou.jul or 0), int(mou.aug or 0), int(mou.sep or 0), int(mou.okt or 0), int(mou.nov or 0), int(mou.des or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print(sum(lrpa_realisasi), " - ", lrpa_realisasi[month-1], " + ", mou_realisasi[month+1])
                except ValueError:
                    mou_realisasi = [int(float(mou.jan) or 0), int(float(mou.feb) or 0), int(float(mou.mar) or 0), int(float(mou.apr) or 0), int(float(mou.mei) or 0), int(float(mou.jun) or 0), int(float(mou.jul) or 0), int(float(mou.aug) or 0), int(float(mou.sep) or 0), int(float(mou.okt) or 0), int(float(mou.nov) or 0), int(float(mou.des) or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print("FLOAT")
                except MouPengalihanData.DoesNotExist:
                    temp_realisasi_temp = sum(lrpa_realisasi)

                temp_realisasi = temp_realisasi + temp_realisasi_temp
                count_bpo = count_bpo + 1
            
            count_bpo_total = count_bpo_total + count_bpo
            
            total_ai_bpo = total_ai_bpo + sum_ai_temp
            total_aki_bpo = total_aki_bpo + sum_aki_temp
            total_realisasi_bpo = total_realisasi_bpo + temp_realisasi

            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            BPO_list.append((BPO_UPP_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct,count_bpo))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
            count_bpo = 0
        
        context["BPO_list"] = BPO_list

        context["count_bpo_total"] = count_bpo_total
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

        count_a_total = 0
        count_a = 0
        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0

        for idx,x in enumerate(A_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                lrpa_realisasi = [int(lrpa.jan_realisasi_disburse or 0), int(lrpa.feb_realisasi_disburse or 0), int(lrpa.mar_realisasi_disburse or 0), int(lrpa.apr_realisasi_disburse or 0), int(lrpa.mei_realisasi_disburse or 0), int(lrpa.jun_realisasi_disburse or 0), int(lrpa.jul_realisasi_disburse or 0), int(lrpa.aug_realisasi_disburse or 0), int(lrpa.sep_realisasi_disburse or 0), int(lrpa.okt_realisasi_disburse or 0), int(lrpa.nov_realisasi_disburse or 0), int(lrpa.des_realisasi_disburse or 0)]
                try:
                    mou = MouPengalihanData.objects.get(no_prk=p.no_prk, file=last_mou)
                    mou_realisasi = [int(mou.jan or 0), int(mou.feb or 0), int(mou.mar or 0), int(mou.apr or 0), int(mou.mei or 0), int(mou.jun or 0), int(mou.jul or 0), int(mou.aug or 0), int(mou.sep or 0), int(mou.okt or 0), int(mou.nov or 0), int(mou.des or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print(sum(lrpa_realisasi), " - ", lrpa_realisasi[month-1], " + ", mou_realisasi[month+1])
                except ValueError:
                    mou_realisasi = [int(float(mou.jan) or 0), int(float(mou.feb) or 0), int(float(mou.mar) or 0), int(float(mou.apr) or 0), int(float(mou.mei) or 0), int(float(mou.jun) or 0), int(float(mou.jul) or 0), int(float(mou.aug) or 0), int(float(mou.sep) or 0), int(float(mou.okt) or 0), int(float(mou.nov) or 0), int(float(mou.des) or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print("FLOAT")
                except MouPengalihanData.DoesNotExist:
                    temp_realisasi_temp = sum(lrpa_realisasi)

                temp_realisasi = temp_realisasi + temp_realisasi_temp
                count_a = count_a + 1
            
            count_a_total = count_a_total + count_a
            total_ai_a = total_ai_a + sum_ai_temp
            total_aki_a = total_aki_a + sum_aki_temp
            total_realisasi_a = total_realisasi_a + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (temp_realisasi/sum_aki_temp)*100

            A_list.append((A_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct,count_a))

            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0
            count_a = 0

        context["A_list"] = A_list

        context["count_a_total"] = count_a_total
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

        count_b_total = 0
        count_b = 0
        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0
        

        for idx,x in enumerate(B_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                lrpa_realisasi = [int(lrpa.jan_realisasi_disburse or 0), int(lrpa.feb_realisasi_disburse or 0), int(lrpa.mar_realisasi_disburse or 0), int(lrpa.apr_realisasi_disburse or 0), int(lrpa.mei_realisasi_disburse or 0), int(lrpa.jun_realisasi_disburse or 0), int(lrpa.jul_realisasi_disburse or 0), int(lrpa.aug_realisasi_disburse or 0), int(lrpa.sep_realisasi_disburse or 0), int(lrpa.okt_realisasi_disburse or 0), int(lrpa.nov_realisasi_disburse or 0), int(lrpa.des_realisasi_disburse or 0)]
                
                try:
                    mou = MouPengalihanData.objects.get(no_prk=p.no_prk, file=last_mou)
                    mou_realisasi = [int(mou.jan or 0), int(mou.feb or 0), int(mou.mar or 0), int(mou.apr or 0), int(mou.mei or 0), int(mou.jun or 0), int(mou.jul or 0), int(mou.aug or 0), int(mou.sep or 0), int(mou.okt or 0), int(mou.nov or 0), int(mou.des or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print(sum(lrpa_realisasi), " - ", lrpa_realisasi[month-1], " + ", mou_realisasi[month+1])
                except ValueError:
                    mou_realisasi = [int(float(mou.jan) or 0), int(float(mou.feb) or 0), int(float(mou.mar) or 0), int(float(mou.apr) or 0), int(float(mou.mei) or 0), int(float(mou.jun) or 0), int(float(mou.jul) or 0), int(float(mou.aug) or 0), int(float(mou.sep) or 0), int(float(mou.okt) or 0), int(float(mou.nov) or 0), int(float(mou.des) or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print("FLOAT")
                except MouPengalihanData.DoesNotExist:
                    temp_realisasi_temp = sum(lrpa_realisasi)

                temp_realisasi = temp_realisasi + temp_realisasi_temp
                count_b = count_b + 1
            
            count_b_total = count_b_total + count_b
            total_ai_b = total_ai_b + sum_ai_temp
            total_aki_b = total_aki_b + sum_aki_temp
            total_realisasi_b = total_realisasi_b + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            B_list.append((B_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct,count_b))

            count_b = 0
            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["B_list"] = B_list

        context["count_b_total"] = count_b_total
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

        count_c_total = 0
        count_c = 0
        sum_ai_temp = 0
        sum_aki_temp = 0
        temp_realisasi = 0

        for idx,x in enumerate(C_PRK_2):
            prk = PRK_Lookup.objects.filter(file=file_lookup, kode_prk=x)
            for p in prk:
                lrpa = LRPA_Monitoring.objects.get(no_prk=p.no_prk, file=last_lrpa)
                sum_ai_temp = sum_ai_temp + lrpa.real_ai()
                sum_aki_temp = sum_aki_temp + lrpa.real_aki()
                lrpa_realisasi = [int(lrpa.jan_realisasi_disburse or 0), int(lrpa.feb_realisasi_disburse or 0), int(lrpa.mar_realisasi_disburse or 0), int(lrpa.apr_realisasi_disburse or 0), int(lrpa.mei_realisasi_disburse or 0), int(lrpa.jun_realisasi_disburse or 0), int(lrpa.jul_realisasi_disburse or 0), int(lrpa.aug_realisasi_disburse or 0), int(lrpa.sep_realisasi_disburse or 0), int(lrpa.okt_realisasi_disburse or 0), int(lrpa.nov_realisasi_disburse or 0), int(lrpa.des_realisasi_disburse or 0)]
                
                try:
                    mou = MouPengalihanData.objects.get(no_prk=p.no_prk, file=last_mou)
                    mou_realisasi = [int(mou.jan or 0), int(mou.feb or 0), int(mou.mar or 0), int(mou.apr or 0), int(mou.mei or 0), int(mou.jun or 0), int(mou.jul or 0), int(mou.aug or 0), int(mou.sep or 0), int(mou.okt or 0), int(mou.nov or 0), int(mou.des or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print(sum(lrpa_realisasi), " - ", lrpa_realisasi[month-1], " + ", mou_realisasi[month+1])
                except ValueError:
                    mou_realisasi = [int(float(mou.jan) or 0), int(float(mou.feb) or 0), int(float(mou.mar) or 0), int(float(mou.apr) or 0), int(float(mou.mei) or 0), int(float(mou.jun) or 0), int(float(mou.jul) or 0), int(float(mou.aug) or 0), int(float(mou.sep) or 0), int(float(mou.okt) or 0), int(float(mou.nov) or 0), int(float(mou.des) or 0)]
                    temp_realisasi_temp = sum(lrpa_realisasi) - lrpa_realisasi[month-1] + mou_realisasi[month+1]
                    print("FLOAT")
                except MouPengalihanData.DoesNotExist:
                    temp_realisasi_temp = sum(lrpa_realisasi)

                temp_realisasi = temp_realisasi + temp_realisasi_temp
                count_c = count_c + 1
            
            count_c_total = count_c_total + count_c
            total_ai_c = total_ai_c + sum_ai_temp
            total_aki_c = total_aki_c + sum_aki_temp
            total_realisasi_c = total_realisasi_c + temp_realisasi
            
            temp_sisa = sum_aki_temp-temp_realisasi
            temp_pct = (safe_div(temp_realisasi,sum_aki_temp))*100

            C_list.append((C_PRK_1[idx],x,sum_ai_temp,sum_aki_temp,temp_realisasi,temp_sisa,temp_pct,count_c))

            count_c = 0
            sum_ai_temp = 0
            sum_aki_temp = 0
            temp_realisasi = 0

        context["C_list"] = C_list

        context["count_c_total"] = count_c_total
        context["total_ai_c"] = total_ai_c
        context["total_aki_c"] = total_aki_c
        context["total_realisasi_c"] = total_realisasi_c
        context["total_sisa_aki_c"] = total_aki_c - total_realisasi_c
        context["total_pct_c"] = (safe_div(total_realisasi_c,total_aki_c))*100

        total_ai_prk = total_ai_a + total_ai_b + total_ai_c
        total_aki_prk = total_aki_a + total_aki_b + total_aki_c
        total_realisasi_prk = total_realisasi_a + total_realisasi_b + total_realisasi_c
        total_sisa_aki_prk = total_aki_prk - total_realisasi_prk
        total_count_prk = count_a_total + count_b_total + count_c_total

        context["total_count_prk"] = total_count_prk
        context["total_ai_prk"] = total_ai_prk
        context["total_aki_prk"] = total_aki_prk
        context["total_realisasi_prk"] = total_realisasi_prk
        context["total_sisa_aki_prk"] = total_sisa_aki_prk
        context["total_pct_prk"] = (safe_div(total_realisasi_prk,total_aki_prk))*100
        #END COUNT FOR ALL PRK IN "Pekerjaan. Lainnya"

        return render(request, 'monev/monev_view.html', context)

class LKAIView(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context["month"] = this_month()
        #Total: 1.57s Python: 1.26s DB: 0.31s Queries: 14 

        # ALL DOCUMENT NEEDED
        if is_production():
            skai_1 = DocSKAI.objects.get(pk=1)
            skai_2 = DocSKAI.objects.get(pk=3)
            skai_3 = DocSKAI.objects.get(pk=6)
        else:
            skai_1 = DocSKAI.objects.get(pk=8)
            skai_2 = DocSKAI.objects.get(pk=10)
            skai_3 = DocSKAI.objects.get(pk=19)
        
        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        last_mou = FileMouPengalihan.objects.order_by('file_export_date').first()

        sq_1 = MacroData.objects.filter(macro_file=skai_1.macro.macro_file_1, prk=OuterRef('prk'))
        sq_2 = MacroData.objects.filter(macro_file=skai_2.macro.macro_file_1, prk=OuterRef('prk'))
        sq_3 = MacroData.objects.filter(macro_file=skai_3.macro.macro_file_1, prk=OuterRef('prk'))
        sq_mou = MouPengalihanData.objects.filter(file=last_mou, prk=OuterRef('prk'))

        #GET USER DIVISION, DETERMINE USER VIEW
        division = request.user.division

        if division == "Super Admin" or division == "ANG":
            monitoring = LRPA_Monitoring.objects.select_related('prk').filter(file=last_lrpa)
            context["for_div"] = "ALL"
        else:
            monitoring = LRPA_Monitoring.objects.select_related('prk').filter(file=last_lrpa, prk__rekap_user_induk=division)
            context["for_div"] = division
        
        lrpa = monitoring. \
               annotate(ai_1 = Round(sq_1.values('ai_this_year')), aki_1 = Round(sq_1.values('aki_this_year')), status_1 = sq_1.values('ang_status'),
               ai_2 = Round(sq_2.values('ai_this_year')), aki_2 = Round(sq_2.values('aki_this_year')), status_2 = sq_2.values('ang_status'),
               ai_3 = Round(sq_3.values('ai_this_year')), aki_3 = Round(sq_3.values('aki_this_year')), status_3 = sq_3.values('ang_status'),
               mou_jan = sq_mou.values('jan'),mou_feb = sq_mou.values('feb'),mou_mar = sq_mou.values('mar'),mou_apr = sq_mou.values('apr'),
               mou_mei = sq_mou.values('mei'),mou_jun = sq_mou.values('jun'),mou_jul = sq_mou.values('jul'),mou_aug = sq_mou.values('aug'),
               mou_sep = sq_mou.values('sep'),mou_okt = sq_mou.values('okt'),mou_nov = sq_mou.values('nov'),mou_des = sq_mou.values('des'),
               sd_1 = sq_1.values('sumber_dana'), sd_2 = sq_2.values('sumber_dana'), sd_3 = sq_3.values('sumber_dana'),
               )
        
        context["lrpa"] = lrpa

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

class UploadMouPengalihan(LoginRequiredMixin, View):

    def get(self, request):
        context = {}

        return render(request, 'monev/upload_mou.html', context)
    
    def post(self, request):
        context = {}

        file = request.FILES["mou_file"]

        wb = load_workbook(file, data_only=True)
        ws = wb['All Pengalihan']

        start_col = 2
        end_col = 19

        list_rows = [idx for idx,cell in enumerate(ws["C"]) if cell.value and idx >= 8]
        print(list_rows[-1])
        x = list_rows[-1]
        x = x + 1
        list_rows.append(x)
        print(list_rows[-1]) #USE THIS METHOD IN MACROS TOO !!

        doc_form = MouFileForm(request.POST, request.FILES)
        if doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.upload_by = request.user
            doc.save()
            
            for rows in list_rows:
                row = [cell.value for cell in ws[rows][start_col:end_col+1]]

                try:
                    mou = MouPengalihanData(
                        file = doc,
                        no_prk = row[0],
                        mou = row[3],
                        ai_this_year = row[4],
                        aki_this_year = row[5],
                        jan = row[6],
                        feb = row[7],
                        mar = row[8],
                        apr = row[9],
                        mei = row[10],
                        jun = row[11],
                        jul = row[12],
                        aug = row[13],
                        sep = row[14],
                        okt = row[15],
                        nov = row[16],
                        des = row[17]
                    )
                    mou.save()
                except Exception as e:
                    exception_type, exception_object, exception_traceback = sys.exc_info()
                    line_number = exception_traceback.tb_lineno
                    print(e, line_number, exception_type, exception_object)
        else:
            print(doc_form.errors)


        return render(request, 'monev/upload_mou.html', context)


class FileMonevList(LoginRequiredMixin, View):

    def get(self, request):
        context = {}

        doc = FileMouPengalihan.objects.all().order_by('file_export_date')
        lrpa = LRPA_File.objects.all().order_by('file_export_date')
        context["docs"] = doc
        context["lrpa"] = lrpa

        return render(request, 'monev/file_monev.html', context)

class EditPRK(LoginRequiredMixin, View):
    def test_func(self):
        return self.request.user.is_admin or self.request.user.is_staff
    
    def get(self, request):
        pass

    def post(self, request):
        pass

