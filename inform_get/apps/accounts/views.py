from django.shortcuts import render, reverse, redirect,HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# auth主认证模块
from django.contrib import auth
# 对应数据库，可以创建添加记录
from django.contrib.auth.models import User


def login(request):
    next = request.GET.get('next', '')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if next == "":
                return HttpResponseRedirect(reverse('accounts:change_passwd'))
            else:
                return HttpResponseRedirect(next)
        else:
            # 登陆失败
            return render(request, 'login.html')
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect(reverse("accounts:login"))



def reset_passwd(request):
    return render(request, "reset_passwd.html")

@login_required
def change_passwd(request):
    return render(request, "change_passwd.html")


def ldap_set(request):
    return render(request, "ldap_set.html")

# @login_required()
def pause(request):
    return render(request, "pause.html")
# def base(request):
#     return render(request, "base.html")

# @login_required()
def option_rec(request):
    return render(request, "option_rec.html")

# # Create your views here.
# def login(request):
#     if request.method == 'POST':
#         login_form = forms.UserForm(request.POST)
#         message = '请检查填写的内容！'
#         if login_form.is_valid():
#             username = login_form.cleaned_data.get('username')
#             password = login_form.cleaned_data.get('password')
#
#             try:
#                 user = models.User.objects.get(name=username)
#             except :
#                 message = '用户不存在！'
#                 return render(request, 'login/login.html', locals())
#
#             if user.password == password:
#                 return redirect('/index/')
#             else:
#                 message = '密码不正确！'
#                 return render(request, 'login/login.html', locals())
#         else:
#             return render(request, 'login/login.html', locals())
#
#     login_form = forms.UserForm()
#     return render(request, 'login/login.html', locals())
