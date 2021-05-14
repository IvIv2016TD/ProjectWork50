from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#from models import Profile

class SignUpForm(UserCreationForm):
    
    SINGLE_USER = 'SU'
    GROUP_MEMBER = 'GM'
    TEAM_LEADER = 'TL'
    STATUS_OF_USER_CHOICES = [
        (SINGLE_USER, 'Одиночный пользователь'),
        (GROUP_MEMBER, 'Член группы'),
        (TEAM_LEADER, 'Руководитель группы'),
    ]	
    first_name = forms.CharField(max_length=100, label='Имя', help_text='Имя пользователя')
    last_name = forms.CharField(max_length=100, label='Фамилия', help_text='Фамилия пользователя')
    email = forms.EmailField(max_length=150, help_text='Email')
    status_of_user = forms.ChoiceField(choices=STATUS_OF_USER_CHOICES, 
	                                   label='Статус пользователя',
									   help_text='Статус пользователя')
    #status_of_user = forms.CharField(max_length=100, label='Статус пользователя')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2', 'status_of_user',)

class NumberOfPoints(forms.Form):
    #number_of_points = 1000
    number_of_points = forms.IntegerField(label = 'Количество точек тестовой последовательности:', min_value =1, max_value = 1000) 