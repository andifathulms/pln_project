from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from django.db.models import Sum, OuterRef, Subquery, F, Value
from django.db.models.functions import Round
from document.models import DocSKAI, MacroData

from monev.models import LRPA_Monitoring, LRPA_File, MouPengalihanData, FileMouPengalihan
from document.models import PRK
from monev.views import this_month, is_production

from num2words import num2words

class RecompositionAKI(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context["month"] = this_month()
        #Total: 1.57s Python: 1.26s DB: 0.31s Queries: 14 

        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        last_mou = FileMouPengalihan.objects.order_by('file_export_date').first()

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
               annotate(
               mou_jan = sq_mou.values('jan'),mou_feb = sq_mou.values('feb'),mou_mar = sq_mou.values('mar'),mou_apr = sq_mou.values('apr'),
               mou_mei = sq_mou.values('mei'),mou_jun = sq_mou.values('jun'),mou_jul = sq_mou.values('jul'),mou_aug = sq_mou.values('aug'),
               mou_sep = sq_mou.values('sep'),mou_okt = sq_mou.values('okt'),mou_nov = sq_mou.values('nov'),mou_des = sq_mou.values('des')
               )
        
        document = [last_lrpa, last_mou]
        context["document"] = document #OPTIMIZE LATER?

        context["lrpa"] = lrpa

        for data in lrpa:
            print(data.no_prk, data.prk.pk)

        return render(request, 'recomposition/recomposition_aki.html', context)

class UsulanRekomposisiEdit(LoginRequiredMixin, View):
    
    def get(self, request, pk, month, *args, **kwargs):
        context = {}
        months = {1:"Januari", 2:"Februari", 3:"Maret", 4:"April", 5:"Mei", 6:"Juni", 7:"Juli", 8:"Agustus", 9:"September", 10:"Oktober", 11:"November", 12:"Desember"}

        prk = PRK.objects.get(pk=pk)
        context["data"] = prk

        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        prk_lrpa = LRPA_Monitoring.objects.get(file=last_lrpa, prk=prk)
        value = prk_lrpa.get_rencana_bulan(month) #MANUAL

        context["value"] = str(value)
        context["words"] = num2words(value , lang='id')
        context["month"] = months[month]
        context["selisih"] = str(value) #MANUAL

        return render(request, 'recomposition/snippets/modal_edit.html', context)

    def post(self, request, pk, type, *args, **kwargs):
        context = {}

        pass

class OnChangeValue(LoginRequiredMixin, View):

    def get(self, request, former_value):
        context = {}
        data = request.GET
        context["words"] = num2words(int(data["value"]) , lang='id')
        

        selisih = int(data["value"]) - int(former_value)

        if selisih > 0:
            context["selisih"] = str(selisih) + " (tambah)"
        elif selisih < 0:
            context["selisih"] = str(selisih) + " (kurang)"
        else:
            context["selisih"] = str(selisih)

        print(context["selisih"])

        return render(request, 'recomposition/snippets/value_to_words.html', context)
