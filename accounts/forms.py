from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile, Seanses, Groupshr

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
    #name_of_group = forms.ChoiceField(label='Выбор группы',
	#								   help_text='Выберите группу в которой хотите зарегистрироваться')
    
	#choices_of_TL = []
    id_user = Profile.objects.filter(status_of_user=TEAM_LEADER).values_list('id', 'user')	# id всех руководителей групп
    #user_user = User.objects.filter(id=item).values_list('user')
    names_list = []
    i = 0
    for item in id_user:
		#id_user = User.objects.filter(username=item).values_list('id')
        user_user = User.objects.filter(id=id_user[i][1]).values_list('username')
        user_first_name = Profile.objects.filter(id=id_user[i][0]).values_list('first_name')
        user_last_name = Profile.objects.filter(id=id_user[i][0]).values_list('last_name')
        user_full_name = str(user_first_name[0][0]) + " " + str(user_last_name[0][0])	# полное имя руководителя групп
        #names_of_group_TL = Groupshr.objects.filter(id=id_user[i][0]).filter(operating_grouphr="True").values_list('name_of_grouphr')	# список работающих групп выбранного руководителя
        names_of_group_TL = Groupshr.objects.filter(user=user_user[0][0]).filter(operating_grouphr="True").values_list('name_of_grouphr')	# список работающих групп выбранного руководителя
        group_list = []
        #str_return = ''
        j = 0
        for item_group in names_of_group_TL:
            str_return = user_user[0][0] + ' ' + names_of_group_TL[j][0]
            #dict_return = {'name_TL':user_user[0][0], 'group_GM':names_of_group_TL[j][0]}
            group_list.append((str_return, names_of_group_TL[j][0]))
            j = j + 1
        #names_list.append((user_user[0][0], user_user[0][0]))
        #names_list.append((id_user[i][0], user_full_name))
        #names_list.append((item, id_user[i][0]))
        #names_list.append((item, user_first_name[0][0]))
        names_list.append((user_full_name, group_list))
        i = i + 1
	
    #self.fields['name_of_group'].choices = names_list
    name_of_group = forms.ChoiceField(choices=names_list,
	                                  label='Выбор группы')
									  #help_text='Выберите группу в которой хотите зарегистрироваться')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
'email', 'password1', 'password2', 'status_of_user',)

class NumberOfPoints(forms.Form):
    #number_of_points = 1000
    number_of_points = forms.IntegerField(label = 'Количество точек тестовой последовательности:', min_value =1, max_value = 100) 