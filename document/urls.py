from django.urls import path

from .views import(
	UploadSKAI,
    SKAIListView,
    LKAIView,
    SKAIComparison,
    SKAIDeleteView,
    SKAIUpdateView,
)

app_name = 'document'

urlpatterns = [
    path('upload-skai', UploadSKAI.as_view(), name='doc-upload-skai'),
    path('list-skai/<int:pk>/', SKAIListView.as_view(), name='doc-list-skai'),
    path('lkai-view/<int:pk>/', LKAIView.as_view(), name='doc-view-lkai'),
    path('skai-comparison', SKAIComparison.as_view(), name='doc-skai-compare'),
    
    path('delete-skai/<int:pk>/', SKAIDeleteView.as_view(), name='doc-skai-delete'),
    path('update-skai/<int:pk>/', SKAIUpdateView.as_view(), name='doc-skai-update'),
]