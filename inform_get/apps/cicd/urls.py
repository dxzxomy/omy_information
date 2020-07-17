from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.static import serve

urlpatterns = [
    url(r'^$', views.get_ou, name='get_ou'),
    url(r'^users', views.users, name='users')

]