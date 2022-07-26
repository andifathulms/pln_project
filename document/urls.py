from django.urls import path

from .views import(
	UploadSKAI,
    UploadLKAI,
    SKAIListView,
    LKAIListView,
    MacroView,
    SKAIComparison,
    pdfViewer,
)

app_name = 'document'

urlpatterns = [
    path('upload-skai', UploadSKAI.as_view(), name='doc-upload-skai'),
    path('upload-lkai', UploadLKAI.as_view(), name='doc-upload-lkai'),
    path('list-skai', SKAIListView.as_view(), name='doc-list-skai'),
    path('list-lkai', LKAIListView.as_view(), name='doc-list-lkai'),
    path('skai-comparison', SKAIComparison.as_view(), name='doc-skai-compare'),
    path('macro-view/<int:pk>/', MacroView.as_view(), name='doc-macro-view'),
    path('pdf-view/<int:pk>/', pdfViewer, name='pdf-viewer'),
]