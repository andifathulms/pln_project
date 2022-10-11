from django.urls import path

from .views import(
    LoginHistory,
)

app_name = 'account'

urlpatterns = [
    path('login-history', LoginHistory.as_view(), name='login-history'),
]