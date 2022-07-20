from django.urls import path

from .views import(
	export,
    simple_upload,
	upload_anyway,
    DummyTableListView,
    DummyView,
)

app_name = 'dummy'

urlpatterns = [
    path('', DummyTableListView.as_view(), name='dummy-list'),
    path('dummy/', DummyView.as_view(), name='dummy-dummy'),
	path('export/', export, name='dummy-export'),
	path('simple_upload/', simple_upload, name='dummy-upload'),
    path('upload_anyway/', upload_anyway, name='dummy-uploadx'),
]