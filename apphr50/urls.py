from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('comein/', views.comein, name='comein'),
    path('about/', views.about, name='about'),
    path('whatfor/', views.whatfor, name='whatfor'),
    path('howtouse/', views.howtouse, name='howtouse'),
    path('registration/', views.registration, name='registration'),
#    path('home/', views.home, name='home'),     
]