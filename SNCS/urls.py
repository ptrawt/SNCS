"""SNCS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import RedirectView
from website import views

urlpatterns = [
    path('SNCS/', views.index),
    path('SNCS/index.html', views.index),
    path('SNCS/login.html', views.login),
    path('SNCS/register.html', views.register),
    path('SNCS/d1config.html', views.d1config),
    path('SNCS/commandLine.html', views.cmd),
    path('SNCS/rack_detail.html', views.rack_detail),
    path('SNCS/node_detail.html', views.node_detail),
    path('SNCS/template_file.html', views.template_file),

]
