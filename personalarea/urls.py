# personalarea/urls.py
from django.urls import path, include
#from . import views 
from .views import prsar_view, logged_out_view, work_with_seanses, work_with_series, work_with_points, testing, prsar_reggr_view, grouphr_create 
#from apphr50.views import index
 
urlpatterns = [
    #path('personalarea/prsar/', prsar_view, name='prsar'),
    #path('prsar_reggr/', prsar_reggr_view, name='prsar_reggr'),	
    path('personalarea/logged_out/', logged_out_view, name='logged_out'),
    path('work_with_seanses/', work_with_seanses, name='work_with_seanses'),
    path('work_with_series/', work_with_series, name='work_with_series'),
    path('work_with_points/', work_with_points, name='work_with_points'),
    path('testing/', testing, name='testing'),
    path('grouphr_create/', grouphr_create, name='grouphr_create'),
]