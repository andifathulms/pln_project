from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponse

from .models import DummyTable, DummyFileUpload
from .forms import DummyFileUploadForm
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

        year = DummyFileUpload.objects.values("year").distinct()
        context['year'] = year

        return render(request, 'dummy/dummy_list.html', context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        dummy_file = DummyFileUpload.objects.get(year=request.POST["year"], status=request.POST["status"])
        dummy = DummyTable.objects.filter(dummy_file=dummy_file)
        context['dummys'] = dummy
        context['dummy_file'] = dummy_file

        year = DummyFileUpload.objects.values("year").distinct()
        context['year'] = year

        return render(request, 'dummy/dummy_list.html', context)

#obsolete, just for view
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
    context = {}
    if request.method == 'POST':
        dataset = Dataset()
        new_dummytable  = request.FILES['myfile']

        filename = request.FILES.get('myfile').name
        context["filename"] = filename

        imported_data = dataset.load(new_dummytable.read(), format='xlsx')
        #if not DummyTable.objects.filter(name=filename).exists():
        if True:
            #Save data to DummyFileUpload
            print(request.POST)
            dummy_file_form = DummyFileUploadForm(request.POST)
            if dummy_file_form.is_valid():
                new_dummy_file = dummy_file_form.save(commit=False)
                new_dummy_file.uploader = request.user
                new_dummy_file.filename = filename
                new_dummy_file.save()

                #Save data to DummyTable
                for data in imported_data:
                    value = DummyTable(name=filename, 
                                    field1=data[0],
                                    field2=data[1],
                                    field3=data[2],
                                    field4=data[3],
                                    dummy_file=new_dummy_file)
                    value.save()
            else:
                print(dummy_file_form.errors)

        else:
            return render(request, 'snippets/already_exist_file.html', context)

    dummyfiles = DummyFileUpload.objects.all()
    context["dummyfiles"] = dummyfiles

    return render(request, 'dummy/input.html', context)

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

