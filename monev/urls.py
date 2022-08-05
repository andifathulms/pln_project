from django.urls import path

from .views import(
	MonevView,
)

app_name = 'monev'

urlpatterns = [
    path('monev-view', MonevView.as_view(), name='monev-view'),
]