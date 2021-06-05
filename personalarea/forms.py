from django import forms
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

#from models import Profile

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

class SimpleForm(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )