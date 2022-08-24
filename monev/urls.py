from django.urls import path

from .views import(
    MonevView,
	LKAIView,
    UploadLRPA,
    UploadMouPengalihan,
    LRPAList,
    PengalihanList,
    ReferenceLookup,
)

app_name = 'monev'

urlpatterns = [
    path('monev-lkai', LKAIView.as_view(), name='lkai-view'),
    path('lrpa-upload', UploadLRPA.as_view(), name='monev-upload-lrpa'),
    path('lrpa-list', LRPAList.as_view(), name='monev-list-lrpa'), 
    path('monev-view', MonevView.as_view(), name='monev-view'),
    path('pengalihan-list', PengalihanList.as_view(), name='monev-list-pengalihan'),
    path('mou-upload', UploadMouPengalihan.as_view(), name='monev-upload-mou'),
    path('reference-lookup', ReferenceLookup.as_view(), name='monev-reference-lookup'),
]