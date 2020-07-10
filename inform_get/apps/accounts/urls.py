from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.passwd, name='pwd'),
    url(r'^ldap_set', views.ldap_set, name="ldap_set"),
    url(r'^pause', views.pause, name="pause"),
    url(r'^option_rec', views.option_rec, name="option_rec")
    # url(r'^$', views.base, name="base")

]