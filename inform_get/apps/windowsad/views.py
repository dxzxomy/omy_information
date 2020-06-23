from django.shortcuts import HttpResponse,render


def index(request):
    return render(request, 'change_passwd.html')