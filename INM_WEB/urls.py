"""INM_WEB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import path
from ADMIN import views
from WEB import views as views2

urlpatterns = [
    url('index/', views2.index),
    url('login/', views2.login),
    url('registrar/', views2.registrar),
    url('qr/', views.qr),
    url('si/', views.si),
    url('ctpdf/', views.ctpdf),
    path('crud/<str:tabla>', views.crud),
    path('crud/<str:tabla>/<int:id>', views.crud),
    path('importar_paises/', views.importar_paises)
]
