# accounts/urls.py
from django.urls import path
from . import views 
from .views import SignUpView
from accounts.views import home_view, signup_view, activation_sent_view, activation_sent_tl_view, activation_invalid_view, activate
from personalarea.views import prsar_view, grouphr_create, prsar_reggr_view, turn_on, turn_off
from django.contrib import admin
 
urlpatterns = [
	path('login/test_IDB/', views.test_IDB, name='test_IDB'),
    path('login/prsar/', prsar_view, name='prsar'),
    path('login/prsar_reggr/', prsar_reggr_view, name='prsar_reggr'),
    path('login/grouphr_create/', grouphr_create, name='grouphr_create'),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup"),
	path('sent/', activation_sent_view, name="activation_sent"),
	path('sent/gm/', activation_sent_tl_view, name="activation_sent_tl"),	
	path('signup/', activation_invalid_view, name="activation_invalid"),	
	path('activate/<slug:uidb64>/<slug:token>/', activate, name="activate"),
]