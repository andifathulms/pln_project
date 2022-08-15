from django.urls import path

from .views import(
	MonevView,
    UploadLRPA,
    LRPAList,
)

app_name = 'monev'

urlpatterns = [
    path('monev-view', MonevView.as_view(), name='monev-view'),
    path('lrpa-upload', UploadLRPA.as_view(), name='monev-upload-lrpa'),
    path('lrpa-list', LRPAList.as_view(), name='monev-list-lrpa'),
]