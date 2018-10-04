#from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from website import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    # path('SNCS/login', views.login),
    # path('SNCS/register', views.register),
    url(r'^d1config/(?P<sn>[^/]+)/$', views.d1config),
    url(r'^commandLine/(?P<sn>[^/]+)/$', views.cmd),
    url(r'^rack_detail/(?P<ip>[^/]+)/$', views.rack_detail),
    url(r'^node_detail/(?P<ip>[^/]+)/(?P<sn>[^/]+)/$', views.node_detail),
    url(r'^template_file/', views.template_file),

]

urlpatterns += staticfiles_urlpatterns()