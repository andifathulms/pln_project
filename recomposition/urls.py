from django.urls import path

from .views import(
	RecompositionAKI,
    UsulanRekomposisiEdit,
)

app_name = 'recomposition'

urlpatterns = [
    path('recomposition-aki', RecompositionAKI.as_view(), name='recomposition-aki'),
     path('edit-prk/<int:pk>/<int:month>/', UsulanRekomposisiEdit.as_view(), name='recomposition-edit-prk'),
]