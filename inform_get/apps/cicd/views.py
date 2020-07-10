from django.shortcuts import render

# Create your views here.
def get_ou(request):
    pass

def user_info(request):
    return render(request, 'user_info.html')