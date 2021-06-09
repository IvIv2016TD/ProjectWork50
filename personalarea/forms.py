from django import forms
from datetime import *
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

class UsersSeanses_0(forms.Form):
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    favorite_colors = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=FAVORITE_COLORS_CHOICES,
    )

class UsersSeanses(forms.Form):

    seanses_of_user = forms.MultipleChoiceField(label='Сеансы пользователя', help_text='Выберите сеансы с которыми будете работать')
	
    def __init__(self, *args, **username_dict):
        user_auth_name = username_dict.pop('username')
        tb_test = username_dict.pop('tb')
        super(UsersSeanses, self).__init__(*args, **username_dict)

        choices_of_seanses = []
        user_seanses = Seanses.objects.filter(user=user_auth_name)
        delta = timedelta(hours=7, minutes=0)
        i = 0
        for item in user_seanses:
            n_seanse = user_seanses.values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')[i][0]
            begin_seanse = user_seanses.values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')[i][1] + delta
            end_seanse = user_seanses.values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')[i][2] + delta
            points_write = user_seanses.values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')[i][3]
            points_read = user_seanses.values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')[i][4]
            choice_str = begin_seanse.strftime('%d/%m/%Y, %H:%M:') + "  " + end_seanse.strftime('%d/%m/%Y, %H:%M:') + "  " + str(points_write)+ "  " + str(points_read)			
            choices_of_seanses.append ((n_seanse, choice_str))
            i = i + 1

        self.fields['seanses_of_user'].choices = choices_of_seanses

    class Meta:
        model = Seanses
        fields = ('id', 'time_of_begin',)		