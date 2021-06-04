from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#from models import Profile

class NumberOfPoints(forms.Form):
    #number_of_points = 1000
    number_of_points = forms.IntegerField(label = 'Количество точек тестовой последовательности:', min_value =1, max_value = 100) 