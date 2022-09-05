from django.urls import path

from .views import(
	RecompositionAKI,
    UsulanRekomposisiEdit,
    OnChangeValue,
    InlineAKBEdit,
)

app_name = 'recomposition'

urlpatterns = [
    path('recomposition-aki', RecompositionAKI.as_view(), name='recomposition-aki'),
    path('edit-prk/<int:pk>/<int:month>/', UsulanRekomposisiEdit.as_view(), name='recomposition-edit-prk'),
    path('onchgvalue/<int:former_value>/', OnChangeValue.as_view(), name='recomposition-onchgvalue'),
    path('akb-edit/', InlineAKBEdit.as_view(), name='akb-edit'),
]