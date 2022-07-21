from django.urls import path

from .views import(
	UploadSKAI,
    SKAIListView,
    pdfViewer
)

app_name = 'document'

urlpatterns = [
    path('upload-skai', UploadSKAI.as_view(), name='doc-upload-skai'),
    path('list-skai', SKAIListView.as_view(), name='doc-list-skai'),
    path('pdf-view/<int:pk>/', pdfViewer, name='pdf-viewer'),
]