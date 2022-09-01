from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from django.db.models import Sum, OuterRef, Subquery, F, Value
from django.db.models.functions import Round
from document.models import DocSKAI, MacroData

from monev.models import LRPA_Monitoring, LRPA_File, MouPengalihanData, FileMouPengalihan
from monev.views import this_month, is_production

class RecompositionAKI(LoginRequiredMixin, View):

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
               annotate(ai_1 = Round(Subquery(sq_1.values('ai_this_year')[:1])*1000), aki_1 = Round(Subquery(sq_1.values('aki_this_year')[:1])*1000), status_1 = sq_1.values('ang_status'),
               ai_2 = Round(Subquery(sq_2.values('ai_this_year')[:1])*1000), aki_2 = Round(Subquery(sq_2.values('aki_this_year')[:1])*1000), status_2 = sq_2.values('ang_status'),
               ai_3 = Round(Subquery(sq_3.values('ai_this_year')[:1])*1000), aki_3 = Round(Subquery(sq_3.values('aki_this_year')[:1])*1000), status_3 = sq_3.values('ang_status'),
               mou_jan = sq_mou.values('jan'),mou_feb = sq_mou.values('feb'),mou_mar = sq_mou.values('mar'),mou_apr = sq_mou.values('apr'),
               mou_mei = sq_mou.values('mei'),mou_jun = sq_mou.values('jun'),mou_jul = sq_mou.values('jul'),mou_aug = sq_mou.values('aug'),
               mou_sep = sq_mou.values('sep'),mou_okt = sq_mou.values('okt'),mou_nov = sq_mou.values('nov'),mou_des = sq_mou.values('des'),
               sd_1 = sq_1.values('sumber_dana'), sd_2 = sq_2.values('sumber_dana'), sd_3 = sq_3.values('sumber_dana'),
               )
        
        document = [skai_1, skai_2, last_lrpa, skai_3, last_mou]
        context["document"] = document #OPTIMIZE LATER?

        context["lrpa"] = lrpa

        for data in lrpa:
            print(data.no_prk, data.prk.pk)

        return render(request, 'recomposition/recomposition_aki.html', context)
