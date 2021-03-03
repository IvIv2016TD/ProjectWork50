from django.shortcuts import render, get_object_or_404
#from .models import User
from django.utils import timezone

from django.http import HttpResponse


def index(request):
#    return HttpResponse("Приложение apphr50.")
    return render(request, 'apphr50/index_temp.html', {})

def comein(request):
    return render(request, 'apphr50/comein_temp.html', {})
    
def about(request):
    return render(request, 'apphr50/about_temp.html', {})

def whatfor(request):
    return render(request, 'apphr50/whatfor_temp.html', {})

def howtouse(request):
    return render(request, 'apphr50/howtouse_temp.html', {})
    
def registration(request):
    return render(request, 'apphr50/registration_temp.html', {})

#def home(request):
#    return render(request, 'apphr41/home.html', {})    