from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from .models import Document, DocSKAI, DocAddedSKAI
from .forms import DocumentForm

from itertools import chain

class SKAIListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        doc_skai = DocSKAI.objects.all()
        doc_added = DocAddedSKAI.objects.all()
        context["doc_skai"] = list(chain(doc_skai, doc_added))

        # year = DummyFileUpload.objects.values("year").distinct()
        # context['year'] = year

        return render(request, 'document/list_skai.html', context)
    
    def post(self, request, *args, **kwargs):
        pass

class UploadSKAI(LoginRequiredMixin, View):
    
    #doc_skai = DocSKAI.objects.all()

    def get(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        doc_added = DocAddedSKAI.objects.all()
        context["doc_skai"] = list(chain(doc_skai, doc_added))
        return render(request, 'document/upload_SKAI.html', context)

    
    def post(self, request, *args, **kwargs):
        context = {}
        doc_skai = DocSKAI.objects.all()
        doc_added = DocAddedSKAI.objects.all()
        context["doc_skai"] = list(chain(doc_skai, doc_added))
        if 'submit-skai' in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI(document=doc, year=request.POST['year'],revision=False)
                skai.save()
            else:
                print(doc.errors)
        elif 'submit-skai-rev' in request.POST:
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI(document=doc, year=request.POST['year'],revision=True,revision_number=request.POST['rev_number'])
                skai.save()
        elif 'submit-aki' in request.POST:
            print("submit")
            doc_form = DocumentForm(request.POST, request.FILES)
            if doc_form.is_valid():
                doc = doc_form.save(commit=False)
                doc.uploader = request.user
                doc.save()

                skai = DocSKAI.objects.get(id=request.POST["skai"])

                aki = DocAddedSKAI(document=doc, revision_on=skai, revision_number=request.POST["revision_number"])
                aki.save()
            else:
                print(doc_form.errors)

                # aki = DocAddedSKAI(document=doc, )

        return render(request, 'document/upload_SKAI.html', context)

def pdfViewer(request, pk):
    context = {}
    document = Document.objects.get(pk=pk)
    context["url"] = document.file.url

    return render(request, 'pdfjs.html', context)


