from django.shortcuts import render
from libs.ldap_users import UserLdap
import json
# Create your views here.
def get_ou(request):
    pass

def users(request):
    g = UserLdap()
    ret_info = g.get_userinfo()
    return render(request, 'user_info.html' ,{"ret_info": ret_info})