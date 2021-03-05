# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.http  import  HttpResponse
import datetime

def home(request):
    return render(request, 'accounts/home.html', {})
	
def about_test(request):
    test_IDB_1(3)
	#console.log('Привет')
	#print("test_IDB_1")
    #return  HttpResponse ('Тест about')
    #return render(request, 'accounts/about_test.html', {})
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)	
	
#def test_IDB_1(request):
#    numpoints = request.POST[number_of_points]
	#return  HttpResponse ('Тест test_IDB')
	#print(numpoints)
 
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

def home_view(request):
    return render(request, 'accounts/home.html')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})	
