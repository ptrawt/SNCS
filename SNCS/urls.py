from django.urls import path
from website import views

urlpatterns = {
    path('SNCS/index', views.index),
    path('SNCS/login', views.login),
    path('SNCS/register', views.register),
    path('SNCS/d1config/<str:sn>', views.d1config),
    path('SNCS/commandLine', views.cmd),
    path('SNCS/rack_detail/<str:ip>', views.rack_detail),
    path('SNCS/node_detail/<str:ip>/<str:sn>', views.node_detail),
    path('SNCS/template_file', views.template_file),

}