from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

from document.models import DocSKAI, MacroData

class MonevView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        #skai_1 = DocSKAI.objects.get(pk=8) #DEV
        skai_1 = DocSKAI.objects.get(pk=1) #PROD
        macro_1 = skai_1.macro.macro_file_1
        macro_data_1 = MacroData.objects.filter(macro_file=macro_1)

        #skai_2 = DocSKAI.objects.get(pk=19) #DEV
        skai_2 = DocSKAI.objects.get(pk=6) #PROD
        macro_2 = skai_2.macro.macro_file_1
        macro_data_2 = MacroData.objects.filter(macro_file=macro_2)

        temp_data = MacroData.objects.filter(no_prk="2019.USLS.27.001")
        for d in temp_data:
            print(d.aki_this_year)

        combine_list = []
        #ALL SKIP
        for data in macro_data_1:
            try:
                temp = MacroData.objects.get(no_prk=data.no_prk, macro_file=macro_2)
                if temp.no_prk != None:
                    combine_list.append((data,temp))

                #print(data.macro_file.pk == temp.macro_file.pk)
            except Exception as e:
                #print("Skip " + str(data.no_prk))
                print(e)
        
        context["data"] = combine_list
        return render(request, 'monev/monev_lkai.html', context)
