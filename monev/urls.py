from django.urls import path

from .views import(
    MonevView,
	LKAIView,
    UploadLRPA,
    UploadMouPengalihan,
    FileMonevList,
    EditPRK,
    LKAIViewCOPY,
)

app_name = 'monev'

urlpatterns = [
    path('monev-lkai', LKAIViewCOPY.as_view(), name='lkai-view'),
    path('lrpa-upload', UploadLRPA.as_view(), name='monev-upload-lrpa'),
    path('file-monev-list', FileMonevList.as_view(), name='monev-list-file'), 
    path('monev-view', MonevView.as_view(), name='monev-view'),
    path('mou-upload', UploadMouPengalihan.as_view(), name='monev-upload-mou'),
    path('edit-prk/<int:pk>/<int:type>/', EditPRK.as_view(), name='monev-edit-prk'),
]