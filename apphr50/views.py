from django.shortcuts import render, get_object_or_404
#from .models import User
from django.utils import timezone

from django.http import HttpResponse


def index(request):

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(request, 'apphr50/index_temp.html', context={'num_visits':num_visits}) # num_visits appended


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

