from django import forms
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile, Seanses

BIRTH_YEAR_CHOICES = ['1980', '1981', '1982']
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('black', 'Black'),
]

CONDITIONS = [
    ('rest', 'Покой'),
    ('mixed_load', 'Смешанная нагрузка'),
    ('training', 'Тренировка'),
    ('extreme_load', 'Экстремальная нагрузка'),
]

class NumberOfPoints(forms.Form):
    #number_of_points = 1000
    number_of_points = forms.IntegerField(label = 'Количество точек тестовой последовательности:', min_value =1, max_value = 1440, help_text='Количество точек тестовой последовательности')
    location = forms.CharField(max_length=100, label='Расположение', help_text='Расположение пользователя в процессе записи')
    conditions = forms.ChoiceField(choices=CONDITIONS, label='Условия', help_text='Условия в процессе записи')	

class UsersSeanses(forms.Form):
    def __init__(self, username):
        super().__init__()
        #self.username = "TestUser9"
        conditions = forms.ChoiceField(choices=CONDITIONS, label='Условия', help_text='Условия в процессе записи')	
        user_seanses = Seanses.objects.filter(user=username)
        seanses_of_user = forms.ModelChoiceField(queryset=user_seanses.values_list('user', 'time_of_begin')) 	