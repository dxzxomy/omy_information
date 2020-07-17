from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
# Create your views here.
from libs.ldap_users import UserLdap




def users_ad_info(request):
    g = UserLdap()
    ret_info = g.get_userinfo()
    return JsonResponse(ret_info, safe=False)