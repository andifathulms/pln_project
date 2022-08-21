"""project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from django.conf.urls.static import static
from django.conf import settings

from account.views import login_view, DashboardView, logout_view
from document.views import XLSM_Playground, JSON_Dumps, Assign_PRK
from notification.views import not_found_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name="home"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('not_found/', not_found_404.as_view(), name="not_found"),

    path('document/', include('document.urls', namespace='document')),
    path('monev/', include('monev.urls', namespace='monev')),

    #for dev only
    path('playground/', XLSM_Playground.as_view(), name="playground"),
    path('json-dumps/', JSON_Dumps.as_view(), name="json-dumps"),
    path('assign-prk/', Assign_PRK.as_view(), name="assign-prk"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)