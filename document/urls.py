from django.urls import path

from .views import(
	UploadSKAI,
    SKAIListView,
    LKAIListView,
    SKAIComparison,
    SKAIDeleteView,
)

app_name = 'document'

urlpatterns = [
    path('upload-skai', UploadSKAI.as_view(), name='doc-upload-skai'),
    path('list-skai', SKAIListView.as_view(), name='doc-list-skai'),
    path('list-lkai', LKAIListView.as_view(), name='doc-list-lkai'),
    path('skai-comparison', SKAIComparison.as_view(), name='doc-skai-compare'),
    path('delete-skai/<int:pk>/', SKAIDeleteView.as_view(), name='doc-skai-delete'),
]