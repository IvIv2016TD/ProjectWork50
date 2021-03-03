# accounts/urls.py
from django.urls import path
from . import views 
from .views import SignUpView
from accounts.views import home_view, signup_view
from django.contrib import admin
 
urlpatterns = [
#    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/home/', views.home, name='home'),
	path('^about_test/$', views.about_test, name='about_test'),
    path('', home_view, name="home"),
    path('signup/', signup_view, name="signup")
#	path('test_IDB_1/', views.test_IDB_1),
#    path(r'^test_IDB/$', views.test_IDB),
]