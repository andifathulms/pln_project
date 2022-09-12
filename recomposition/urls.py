from django.urls import path

from .views import(
    RecompositionAKI,
    RecompositionPeriodCreate,
    UsulanRekomposisiEdit,
    OnChangeValue,
    InlineAKBEdit,
    InlineAKBDelete,
    RecompositionPeriod,
)

app_name = 'recomposition'

urlpatterns = [
    path('recomposition-aki', RecompositionAKI.as_view(), name='recomposition-aki'),
    path('recomposition-periode', RecompositionPeriod.as_view(), name='recomposition-periode'),
    path('recomposition-periode-create', RecompositionPeriodCreate.as_view(), name='recomposition-periode-create'),
    path('edit-prk/<int:pk>/<int:month>/', UsulanRekomposisiEdit.as_view(), name='recomposition-edit-prk'),
    path('onchgvalue/<int:former_value>/', OnChangeValue.as_view(), name='recomposition-onchgvalue'),
    path('akb-edit/', InlineAKBEdit.as_view(), name='akb-edit'),
    path('akb-delete/', InlineAKBDelete.as_view(), name='akb-delete'),
]