# personalarea/urls.py
from django.urls import path, include
from . import views 
from .views import prsar_view
#from apphr50.views import index
 
urlpatterns = [
    path('personalarea/prsar/', prsar_view, name='prsar'),
    #path('personalarea/logout/', index, name='index'),
]