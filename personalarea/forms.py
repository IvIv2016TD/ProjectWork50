from django import forms
from datetime import *
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile, Seanses, Groupshr

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

CONDITIONS_DICT = {
    'rest': 'Покой',
    'mixed_load': 'Смешанная нагрузка',
    'training': 'Тренировка',
    'extreme_load': 'Экстремальная нагрузка',
}

WORKS_LIVE = [
    ('0', 'Зарегистрировать новую группу'),
    ('1', 'Выключить/включить старую группу'),
    ('2', 'Выключить/включить пользователя'),
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

class UsersPoints(forms.Form):

    names_of_user = forms.MultipleChoiceField(label='Имена пользователей', help_text='Выберите имена пользователей с сериями которых будете работать')
    names_of_locations = forms.MultipleChoiceField(label='Локации', help_text='Выберите локации с сериями которых будете работать')
    names_of_conditions = forms.MultipleChoiceField(label='Условия', help_text='Выберите условия с сериями которых будете работать')    
	
    def __init__(self, *args, **query_params_dict):
    #def __init__(self, **query_params_dict):
        locations = query_params_dict.pop('locations')
        conditions = query_params_dict.pop('conditions')
        names = query_params_dict.pop('username')		
        super(UsersPoints, self).__init__(*args, **query_params_dict)
        #super(UsersPoints, self).__init__(**query_params_dict)

        #test_list = [("1", "Один"), ("2", "Два"), ("3", "Три")]

        names_list = []
        i = 0
        for item in names:
            id_user = User.objects.filter(username=item).values_list('id')
            user_first_name = Profile.objects.filter(user=id_user[0][0]).values_list('first_name')
            user_last_name = Profile.objects.filter(user=id_user[0][0]).values_list('last_name')
            user_full_name = user_first_name[0][0] + " " + user_last_name[0][0]
            #lni = item + " " + str(id_user[0][0]) + " " + user_full_name
            names_list.append((item, user_full_name))
            i = i + 1

        locations_list = []
        i = 0
        for item in locations:
            locations_list.append((item, item))
            i = i + 1

        conditions_list = []
        i = 0
        for item in conditions:
            conditions_list.append((item, CONDITIONS_DICT[item]))
            i = i + 1
        
        self.fields['names_of_user'].choices = names_list
        self.fields['names_of_locations'].choices = locations_list
        self.fields['names_of_conditions'].choices = conditions_list

class RegistrationGrouphr(forms.ModelForm):

    name_of_grouphr = forms.CharField(max_length=100, label='Имя группы', help_text='Имя регистрируемой группы', required=False)
    comment_of_TL = forms.CharField(max_length=1000, label='Комментарий руководителя', help_text='Комментарий руководителя группы', required=False, widget=forms.Textarea)
    operating_grouphr = forms.BooleanField(label='Активировать группу', help_text='Активирует регистрируемую группу', required=False)
	
    def __init__(self, *args, **username_dict):
        user_auth_name = username_dict.pop('username')
        tb_test = username_dict.pop('tb')
        super(RegistrationGrouphr, self).__init__(*args, **username_dict)

        self.fields['user'].initial = user_auth_name
        self.fields['name_of_grouphr'].initial = tb_test
	
    class Meta:
        model = Groupshr
        fields = ('user', 'name_of_grouphr', 'comment_of_TL', 'operating_grouphr',)
        labels = {
            'user': 'Руководитель группы',
        }
        #widgets = {
        #    'user': 'HiddenInput',
        #}		

class RegistrationGrouphr_0(forms.Form):

    name_of_grouphr = forms.CharField(max_length=100, label='Имя группы', help_text='Имя регистрируемой группы', required=False)
    comment_of_TL = forms.CharField(max_length=1000, label='Комментарий руководителя', help_text='Комментарий руководителя группы', required=False)
	
    def __init__(self, *args, **username_dict):
        user_auth_name = username_dict.pop('username')
        tb_test = username_dict.pop('tb')
        super(RegistrationGrouphr, self).__init__(*args, **username_dict)

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

        #self.fields['seanses_of_user'].choices = choices_of_seanses

class WorksForm(forms.Form):
     works_live = forms.ChoiceField(label='Операции', widget=forms.RadioSelect(), choices=WORKS_LIVE, help_text='Выберите операцию над группой/пользователем', required=False)