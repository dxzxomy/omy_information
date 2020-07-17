from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.static import serve

urlpatterns = [
    url(r'^reset_passwd/$', views.reset_passwd, name='reset_passwd'),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$',views.logout, name='logout'),
    url(r'^$', views.change_passwd, name='change_passwd'),
    url(r'^reset_passwd/$', views.reset_passwd, name='reset_passwd'),
    url(r'^ldap_set/$', views.ldap_set, name="ldap_set"),
    url(r'^pause/$', views.pause, name="pause"),
    url(r'^option_rec/$', views.option_rec, name="option_rec")
]