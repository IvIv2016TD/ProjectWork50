# accounts/urls.py
from django.urls import path
from . import views 
from .views import SignUpView
from accounts.views import home_view, signup_view, activation_sent_view, activation_invalid_view, activate
from django.contrib import admin
 
urlpatterns = [
#    path('login/home/', views.home, name='home'),
	path('login/test_IDB/', views.test_IDB, name='test_IDB'),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
	path('sent/', activation_sent_view, name="activation_sent"),
	path('signup/', activation_invalid_view, name="activation_invalid_view"),	
	path('activate/<slug:uidb64>/<slug:token>/', activate, name="activate"),
]