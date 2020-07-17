from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.views.static import serve

urlpatterns = [
    url(r'^user_info/', views.users_ad_info, name='user_info'),
]
