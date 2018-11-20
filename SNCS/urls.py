from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from website import views

app_name = 'website'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^index/$', views.index, name='index'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^config/(?P<sn>[^/]+)/(?P<username>[^/]+)/$', views.d1config2, name='config'),
    url(r'^commandLine/(?P<sn>[^/]+)/(?P<user>[^/]+)/$', views.cmd, name='cmd'),
    url(r'^rack_detail/(?P<ip>[^/]+)/$', views.rack_detail),
    url(r'^node_detail/(?P<ip>[^/]+)/(?P<id>[^/]+)/$', views.node_detail),
    url(r'^template_file/', views.template_file, name='template_file'),
    url(r'^delete/(?P<id>[\d]+)/$', views.delete_base_file, name='delete'),
    url(r'^view_file/(?P<id>[\d]+)/(?P<files>[^/]+)/$', views.view_base_file, name='view_file'),
    url(r'^logging/', views.logging, name='logging'),
    url(r'^cli/(?P<sn>[^/]+)/(?P<username>[^/]+)/$', views.cli, name='cli'),
    url(r'^cli_success/(?P<sn>[^/]+)/$', views.cli_success)
]

urlpatterns += staticfiles_urlpatterns()