from django.urls import path

from .views import(
	MonevView,
    UploadLRPA,
)

app_name = 'monev'

urlpatterns = [
    path('monev-view', MonevView.as_view(), name='monev-view'),
    path('lrpa-upload', UploadLRPA.as_view(), name='monev-upload-lrpa'),
]