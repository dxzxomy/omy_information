from django.shortcuts import render

# Create your views here.
def passwd(request):
    return render(request, "passwd.html")


def ldap_set(request):
    return render(request, "ldap_set.html")


def pause(request):
    return render(request, "pause.html")
# def base(request):
#     return render(request, "base.html")

def option_rec(request):
    return render(request, "option_rec.html")

