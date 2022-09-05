from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from django.db.models import Sum, OuterRef, Subquery, F, Value
from django.db.models.functions import Round
from document.models import DocSKAI, MacroData

from monev.models import LRPA_Monitoring, LRPA_File, MouPengalihanData, FileMouPengalihan
from document.models import PRK
from monev.views import this_month, is_production

from .models import UsulanRekomposisi, UsulanRekomposisiData

from num2words import num2words

class RecompositionAKI(LoginRequiredMixin, View):

    def get(self, request):
        context = {}
        context["month"] = this_month()

        last_lrpa = LRPA_File.objects.order_by('-file_export_date').first()
        last_mou = FileMouPengalihan.objects.order_by('file_export_date').first()

        #GET USER DIVISION, DETERMINE USER VIEW
        division = request.user.division

        if division == "Super Admin" or division == "ANG":
            monitoring = LRPA_Monitoring.objects.select_related('prk').filter(file=last_lrpa)
            context["for_div"] = "ALL"
        else:
            monitoring = LRPA_Monitoring.objects.select_related('prk').filter(file=last_lrpa, prk__rekap_user_induk=division)
            context["for_div"] = division

        # CREATED INSTANCE DRAFT RECOMP IF THE FIRST TIME IN THIS MONTH
        try :
            draft = UsulanRekomposisi.objects.get(division=context["for_div"], for_month=this_month())
        except:
            draft = UsulanRekomposisi(
                division=context["for_div"],
                for_month=this_month()
            )
            draft.save()

        sq_mou = MouPengalihanData.objects.filter(file=last_mou, prk=OuterRef('prk'))
        sq_edit = UsulanRekomposisiData.objects.filter(file=draft, prk=OuterRef('prk'))
        
        lrpa = monitoring. \
               annotate(
               mou_jan = sq_mou.values('jan'),mou_feb = sq_mou.values('feb'),mou_mar = sq_mou.values('mar'),mou_apr = sq_mou.values('apr'),
               mou_mei = sq_mou.values('mei'),mou_jun = sq_mou.values('jun'),mou_jul = sq_mou.values('jul'),mou_aug = sq_mou.values('aug'),
               mou_sep = sq_mou.values('sep'),mou_okt = sq_mou.values('okt'),mou_nov = sq_mou.values('nov'),mou_des = sq_mou.values('des'),
               edit_jan = sq_edit.values('jan'),edit_feb = sq_edit.values('feb'),edit_mar = sq_edit.values('mar'),edit_apr = sq_edit.values('apr'),
               edit_mei = sq_edit.values('mei'),edit_jun = sq_edit.values('jun'),edit_jul = sq_edit.values('jul'),edit_aug = sq_edit.values('aug'),
               edit_sep = sq_edit.values('sep'),edit_okt = sq_edit.values('okt'),edit_nov = sq_edit.values('nov'),edit_des = sq_edit.values('des')
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
        
        try:
            draft = UsulanRekomposisi.objects.get(division=request.user.division, for_month=this_month())
            prk_draft = UsulanRekomposisiData.objects.get(file=draft, prk=prk)
            value_1 = prk_draft.get_rencana_bulan(month) #MANUAL
        except:
            value_1 = 0

        context["value"] = str(value)

        if value_1:
            context["value_draft"] = str(value_1)
        else:
            context["value_draft"] = str(value)

        context["words"] = num2words(value , lang='id')
        context["this_month"] = month
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

class InlineAKBEdit(LoginRequiredMixin, View):

    def get(self, request):
        pass

    def post(self, request):
        context = {}
        
        data = request.POST
        prk = PRK.objects.get(no_prk = data["no_prk"])
        val = data["value"]

        # GET OR CREATE UsulanRekomposisiData

        # UsulanRekomposisi should be created this time        
        division = request.user.division
        draft = UsulanRekomposisi.objects.get(division=division, for_month=this_month()) #add period later
        try:
            data_rekom = UsulanRekomposisiData.objects.get(file=draft, prk=prk)
            data_rekom.insertToMonth(data["this_month"], int(val))
        except:
            data_rekom = UsulanRekomposisiData(file=draft, prk=prk)
            data_rekom.save()
            data_rekom.insertToMonth(data["this_month"], int(val))

        edit_akb = val
        context["edit_akb"] = edit_akb
        context["data"] = prk
        context["this_month"] = data["this_month"]

        return render(request, 'recomposition/snippets/inline_edit_cell_akb.html', context)
