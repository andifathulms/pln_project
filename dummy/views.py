from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponse

from .models import DummyTable
from .resources import DummyTableResource

from django.contrib import messages
from tablib import Dataset

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class DummyTableListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        dummy = DummyTable.objects.all()
        context['dummys'] = dummy

        return render(request, 'dummy/dummy_list.html', context)

class DummyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        dummy = DummyTable.objects.all()
        context['dummys'] = dummy

        return render(request, 'dummy/dummy_dummy.html', context)

def export(request):
    dummytable_resource = DummyTableResource()
    dataset = dummytable_resource.export()
    response = HttpResponse(dataset.xls, content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

def simple_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_dummytable  = request.FILES['myfile']
        filename = request.FILES.get('myfile').name
        imported_data = dataset.load(new_dummytable.read(), format='xlsx')
        if not DummyTable.objects.filter(name=filename).exists():
            for data in imported_data:
                value = DummyTable(name=filename, 
                                   field1=data[0],
                                   field2=data[1],
                                   field3=data[2],
                                   field4=data[3])
                value.save()
        else:
            return render(request, 'snippets/already_exist_file.html', {'filename':filename})

    return render(request, 'dummy/input.html')

def upload_anyway(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_dummytable  = request.FILES['myfile']
        filename = request.FILES.get('myfile').name
        imported_data = dataset.load(new_dummytable.read(), format='xlsx')
        
        for data in imported_data:
            value = DummyTable(name=filename, 
                                field1=data[0],
                                field2=data[1],
                                field3=data[2],
                                field4=data[3])
            value.save()
    return render(request, 'dummy/input.html')

