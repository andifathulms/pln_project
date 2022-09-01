from django.urls import path

from .views import(
	RecompositionAKI,
)

app_name = 'recomposition'

urlpatterns = [
    path('recomposition-aki', RecompositionAKI.as_view(), name='recomposition-aki'),
]