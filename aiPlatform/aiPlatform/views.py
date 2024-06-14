
from django.shortcuts import render

def login(request):
    return render(request,"login.html")

def adminuser(request):

    return render(request,"adminusers.html")


from django.templatetags.static import static

