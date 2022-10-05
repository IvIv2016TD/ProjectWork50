from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from accounts.models import Profile, Seanses, Groupshr
from datetime import datetime, timedelta
from pandas import *

from .forms import NumberOfPoints, UsersSeanses, UsersPoints, WorksForm, RegistrationGrouphr

#import "influxdata/influxdb/schema"

BUCKET = "HRWEB"
ORG = "PM72"
TOKEN = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
URL = "https://eu-central-1-1.aws.cloud2.influxdata.com/"
MEASUREMENT = "hr_measurement"

WORKS_LIVE = [
    ('0', 'Зарегистрировать новую группу'),
    ('1', 'Отключить/подключить старую группу'),
    ('2', 'Отключить/подключить пользователя'),
]

WORKS_LIVE_DICT = {
    '0':'Зарегистрировать новую группу',
    '1':'Выключить/включить старую группу',
    '2':'Выключить/включить пользователя',
}

CONDITIONS_DICT = {
    'rest': 'Покой',
    'min_load': 'Минимальная нагрузка',
    'mixed_load': 'Смешанная нагрузка',
    'training': 'Тренировка',
    'extreme_load': 'Экстремальная нагрузка',
}

NAME_COL_LIST = [
    "Покой", 
    "Минимальная нагрузка", 
    "Смешанная нагрузка", 
    "Тренировка", 
    "Экстремальная нагрузка"
]

def prsar_view(request):
    
    global tdicprsar    # Словарь для передачи параметров
    
    user = request.user.username
    tdicprsar = {'username':user}
    user_seanses = Seanses.objects.filter(user=user)
    tdicprsar.update({'user_seanses':user_seanses})	
    num_seanses = len(user_seanses)
    tdicprsar.update({'num_seanses':num_seanses})
    time_of_last_visit = user_seanses.values_list('time_of_begin', flat=True).last()
    tdicprsar.update({'time_of_last_visit':time_of_last_visit})
    tdicprsar.update({'time_of_begin':datetime.now()})

    number_of_points_write = 0
    tdicprsar.update({'number_of_points_write':number_of_points_write})
    number_of_points_read = 0
    tdicprsar.update({'number_of_points_read':number_of_points_read})

    tl_groups = Groupshr.objects.filter(user=user)
    n_grouphr = tl_groups.values_list('name_of_grouphr', 'time_of_registration', 'comment_of_TL', 'operating_grouphr')
    tdicprsar.update({'n_grouphr':n_grouphr})    
    
    tdicprsar.update({'Flag_Seanses':0})
    tdicprsar.update({'Flag_Series':0})        

    tdicprsar.update({'name_of_grouphr':'form.not_POST'})
    if request.POST:# and request.is_ajax():
        tdicprsar.update({'name_of_grouphr':'form.POST'})
        form = RegistrationGrouphr(request.POST, username=tdicprsar['username'], tb='')
        if form.is_valid():
            name_of_grouphr = form.cleaned_data.get('name_of_grouphr')
            tdicprsar.update({'name_of_grouphr':'form.is_valid'})
            form.save()
        else:
            errors = form.errors.as_json()
            tdicprsar.update({'name_of_grouphr':'form.is_not_valid'})
            return JsonResponse({"errors": errors}, status=400)		
    else:
        form = RegistrationGrouphr(username=tdicprsar['username'], tb='')
    tdicprsar.update({'form':form})
    tdicprsar.update({'WORKS_LIVE':WORKS_LIVE})
    
    return render(request, 'prsar.html', context=tdicprsar)

def prsar_reggr_view(request):
    tdicprsar.update({'TestGC':'prsar_reggr_view'})
    tdicprsar.update({'TestPRV':prv})

    if request.POST:
        if tdicprsar['form_0'].is_valid():
            name_of_grouphr = form_0.cleaned_data.get('name_of_grouphr')
            comment_of_TL = form_0.cleaned_data.get('comment_of_TL')
            tdicprsar.update({'name_of_grouphr':name_of_grouphr})
            tdicprsar.update({'comment_of_TL':comment_of_TL})
    else:
        form_0 = RegistrationGrouphr(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
    tdicprsar.update({'form_0':form_0})

    return render(request, 'prsar_reggr.html', context=tdicprsar)
	
def logged_out_view():

    # Запись в БД информации о сеансе после записи тестовой последовательности в InfluxBD
    
    seanse = Seanses.create_seanse(tdicprsar['username'], tdicprsar['time_of_begin'],
                tdicprsar['number_of_points_write'], tdicprsar['number_of_points_read'])	
    seanse.save()

    return
    
def logged_out_view_debag(request):

    # Выход из личного кабинета

    logout(request)	
    return render(request, 'logged_out.html', context=tdicprsar)    

def write_influxDB():

    # Вычисление точек тестовой последовательности и запись из в InfluxDB

    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    import random

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    npoints = tdicprsar['number_of_points_write'] 
    tdicprsar.update({'hr_measurement':MEASUREMENT})
    # Сдвиг по условиям
    
    sdv_dict = {
        'rest': 0,
        'min_load': 5,
        'mixed_load': 10,
        'training': 15,
        'extreme_load': 20,
    }
  
    sdv_cond = sdv_dict[tdicprsar['conditions']] + random.randint(-3, 3)
    min = -5
    max = 15
    for item in range(tdicprsar['number_of_points_write']):
        hr = 70 + random.randint(min, max) + sdv_cond
        p = influxdb_client.Point(tdicprsar['hr_measurement']).tag("username", tdicprsar['username']).tag("location", tdicprsar['location']).tag("conditions", tdicprsar['conditions']).field("hr_per_minute", hr)
        write_api.write(bucket=BUCKET, org=ORG, record=p)
    
    return        

def read_influxDB(points_list):

    # Чтение точек тестовой последовательности из InfluxDB

    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    query_api = client.query_api()
    username = '"' + tdicprsar['username'] + '"'
    bucket = '"' + BUCKET + '"'
    measurement = '"' + MEASUREMENT + '"'

    query = 'from(bucket:' + bucket + ')\
    |> range(start: -10m)\
	|> filter(fn:(r) => r._measurement == ' + measurement + ')\
    |> filter(fn:(r) => r.username == ' + username + ')\
    |> filter(fn:(r) => r.location == "Новосибирск")\
    |> filter(fn:(r) => r._field == "hr_per_minute" )'

    result = client.query_api().query(org=ORG, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.values.get('location'), record.get_time(), record.get_field(), record.get_value()))

    delta = timedelta(hours=7, minutes=0)
    for item in results:

        points_list.append("Место " + str(item[0]) + " Дата, время" +
          (item[1] + delta).strftime('%d/%m/%Y, %H:%M:%S') +
          " Имя поля " + str(item[2]) +
          " Значение " + str(item[3])
          )

    tdicprsar.update({'number_of_points_read':len(results)})
    tdicprsar.update({'points_list':points_list})	
	
    return

def read_influxDB_params(points_list, *args, **params_dict):

    # Чтение параметров БД InfluxDB

    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    query_api = client.query_api()
    username = '"' + tdicprsar['username'] + '"'
    bucket = '"' + BUCKET + '"'
    measurement = '"' + MEASUREMENT + '"'
# поправки в 1 секунду из-за скорости передачи точек в InfluxDB - больше 1 точки/секунду
    start_datatime = str(int((params_dict['time_of_begin'] - params_dict['delta_param']).timestamp()) - 1)
    end_datatime = str(int((params_dict['time_of_end']).timestamp()) + 1)
    tdicprsar.update({'TestS':start_datatime})
    tdicprsar.update({'TestE':end_datatime})

    query = 'from(bucket:' + bucket + ')\
    |> range(start: ' + start_datatime + ', stop: ' + end_datatime + ')\
    |> filter(fn:(r) => r._measurement == ' + measurement + ')'

    tdicprsar.update({'TestA':query})

    result = client.query_api().query(org=ORG, query=query)
    tdicprsar.update({'TestRR':len(result)})

    results = []
    for table in result:
        for record in table.records:
            results.append((record.values.get('location'), record.values.get('username'), record.values.get('conditions'), record.get_time(), record.get_field(), record.get_value()))

    tdicprsar.update({'TestRT':len(results)})

    delta = timedelta(hours=7, minutes=0)
    for item in results:

        points_list.append("Место " + str(item[0]) + "Имя пользователя " + str(item[1]) + "Условия " + str(item[2]) +
		  " Дата, время" + (item[3] + delta).strftime('%d/%m/%Y, %H:%M:%S') +
          " Имя поля " + str(item[4]) +
          " Значение " + str(item[5])
          )

    tdicprsar.update({'number_of_points_read':len(results)})
    tdicprsar.update({'points_list':points_list})
    tdicprsar.update({'results':results})	
	
    return

def read_influxDB_DataFrame(points_list, *args, **params_dict):

    # Чтение точек InfluxDB в DataFrame Pandas

    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    query_api = client.query_api()
    username = '"' + tdicprsar['username'] + '"'
    bucket = '"' + BUCKET + '"'
    measurement = '"' + MEASUREMENT + '"'
    start_datatime = str(params_dict['time_of_begin_DF'])
    end_datatime = str(params_dict['time_of_end_DF'])
# формируем строку запроса с фильтрами по имени пользователя
    names_of_user = params_dict['names_of_user']
    names_of_user_str = "("
    for item in names_of_user:
        names_of_user_str = names_of_user_str + "r.username ==" + '"' + item + '"' + " or "
    len_str = len(names_of_user_str) - 4
    names_of_user_str = names_of_user_str[:len_str] + ")"
    tdicprsar.update({'TestNSQ':names_of_user_str})
# формируем строку запроса с фильтрами по локации	
    names_of_locations = params_dict['names_of_locations']
    names_of_locations_str = "("
    for item in names_of_locations:
        names_of_locations_str = names_of_locations_str + "r.location ==" + '"' + item + '"' + " or "
    len_str = len(names_of_locations_str) - 4
    names_of_locations_str = names_of_locations_str[:len_str] + ")"
    tdicprsar.update({'TestLSQ':names_of_locations_str})
# формируем строку запроса с фильтрами по условиям
    names_of_conditions= params_dict['names_of_conditions']
    names_of_conditions_str = "("
    for item in names_of_conditions:
        names_of_conditions_str = names_of_conditions_str + "r.conditions ==" + '"' + item + '"' + " or "
    len_str = len(names_of_conditions_str) - 4
    names_of_conditions_str = names_of_conditions_str[:len_str] + ")"
    tdicprsar.update({'TestСSQ':names_of_conditions_str})
    names_of_all_str = names_of_user_str + " and " + names_of_locations_str + " and " + names_of_conditions_str
    tdicprsar.update({'TestASQ':names_of_all_str})	
    tdicprsar.update({'TestS_DF':start_datatime})
    tdicprsar.update({'TestE_DF':end_datatime})

    query = 'from(bucket:' + bucket + ')\
    |> range(start: ' + start_datatime + ', stop: ' + end_datatime + ')\
    |> filter(fn:(r) => r._measurement == ' + measurement + ')\
    |> filter(fn:(r) => ' + names_of_all_str + ')'

    tdicprsar.update({'TestA':query})

    result = client.query_api().query_data_frame(org=ORG, query=query)
    tdicprsar.update({'TestRR':len(result)})

    delta = timedelta(hours=7, minutes=0)

    tdicprsar.update({'result_DF':result})
    tdicprsar.update({'result':result.to_html()})	
	
    return
	
def work_with_seanses(request):

    # Выбор сеансов работы пользователя

    if request.POST:
        form = UsersSeanses(request.POST, username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
        if form.is_valid():
            tdicprsar.update({'test_POST':'conditionsV'})
            seanses_of_user = form.cleaned_data.get('seanses_of_user')
            tdicprsar.update({'seanses_of_user':seanses_of_user})
    else:
        form = UsersSeanses(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
        tdicprsar.update({'test_POST':'conditionsW'})
    tdicprsar.update({'form':form})    
    return render(request, 'personalarea/work_with_seanses.html', context=tdicprsar)

def work_with_series(request):

    # Выбор серий из выбранных сеансов работы пользователя

    try:
        user_seanses = Seanses.objects.filter(id__in=tdicprsar['seanses_of_user']).values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')
        tdicprsar.update({'Flag_Seanses':1})
        tdicprsar.update({'Flag_Series':0})
    except KeyError:
        tdicprsar.update({'Test_WWP':'Неопределены сеансы'})
        tdicprsar.update({'Flag_Seanses':0})
        return render(request, 'personalarea/work_with_series.html', context=tdicprsar)
    
    tdicprsar.update({'user_seanses':user_seanses})
    args = []
    points_list = []
    params_dict = {}
    results_points_list = []
    i = 0
    for seanse in user_seanses:
        params_dict.update({'user_name':tdicprsar['username']})	# !!!!!!без групп!!!!!!
        params_dict.update({'time_of_begin':user_seanses[i][1]})
        params_dict.update({'time_of_end':user_seanses[i][2]})
        params_dict.update({'delta_param':timedelta(hours=0, minutes=0)})		
        read_influxDB_params(points_list, *args, **params_dict)
        for item in tdicprsar['results']:
            results_points_list.append(item)
        i = i + 1
    list_time_of_point = []
    list_location = []
    list_username = []
    list_conditions = []
# создаём списки значений тегов по всем ключам
    for item in results_points_list:	
        list_location.append(item[0])
        list_username.append(item[1])
        list_conditions.append(item[2])
        list_time_of_point.append(int((item[3]).timestamp()))	# штампы времени всех точек

    time_of_point_begin_stamp = min(list_time_of_point)	# Unix метка времени первой точки совокупности серий
    time_of_point_end_stamp = max(list_time_of_point)	# Unix метка времени последней точки совокупности серий
    params_dict.update({'time_of_begin_DF':time_of_point_begin_stamp})
    params_dict.update({'time_of_end_DF':time_of_point_end_stamp})

# порождаем множества из списков значений тегов для исключения повторяющихся значений
    set_list_location = set(list_location)
    set_list_username = set(list_username)
    set_list_conditions = set(list_conditions)
# порождаем списки уникальных значений тегов по всем ключам
    list_location = []
    list_username = []
    list_conditions = []
    for item in set_list_location:
        list_location.append(item)
    for item in set_list_username:
        list_username.append(item)
    for item in set_list_conditions:
        list_conditions.append(item)
    tdicprsar.update({'list_location':list_location})
    #list_username.append("TestUser2222")
    #list_username.append("TestUser9")
    tdicprsar.update({'list_username':list_username})
    tdicprsar.update({'list_conditions':list_conditions})

    tdicprsar.update({'TestRT':len(results_points_list)})
    tdicprsar.update({'TestUN':len(list_username)})

    #ttt = []
    #ttt.append("ttt1")
    #ttt.append("ttt2")
    #tdicprsar.update({'ttt':ttt})
    #tdicprsar.update({'TestUN':len(ttt)})

    if request.POST:
        form = UsersPoints(request.POST, locations=tdicprsar['list_location'], conditions=tdicprsar['list_conditions'], username=tdicprsar['list_username'])
        if form.is_valid():
            names_of_user = form.cleaned_data.get('names_of_user')
            names_of_locations = form.cleaned_data.get('names_of_locations')
            names_of_conditions= form.cleaned_data.get('names_of_conditions')
# читаем из InfluxDB DataFrame со всеми выбранными сериями
            params_dict.update({'names_of_user':names_of_user})
            params_dict.update({'names_of_locations':names_of_locations})
            params_dict.update({'names_of_conditions':names_of_conditions})

            tdicprsar.update({'names_of_user':names_of_user})
            tdicprsar.update({'names_of_locations':names_of_locations})
            tdicprsar.update({'names_of_conditions':names_of_conditions})
			
            read_influxDB_DataFrame(points_list, *args, **params_dict)

            tdicprsar.update({'Flag_Series':1})
    else:
        form = UsersPoints(locations=tdicprsar['list_location'], conditions=tdicprsar['list_conditions'], username=tdicprsar['list_username'])
    tdicprsar.update({'form':form})
	
    return render(request, 'personalarea/work_with_series.html', context=tdicprsar)

def work_with_points(request):

    # Отображение средних значений выбранных серий на диаграмме

    try:
        result_DF = tdicprsar['result_DF']	# DataFrame результатов
    except KeyError:
        tdicprsar.update({'Test_WWP':'Неопределены серии'})
        return render(request, 'personalarea/work_with_points.html', context=tdicprsar)
    tdicprsar.update({'Test_WWP':'Работа с точками'})
    tdicprsar.update({'Test_MHR':tdicprsar['names_of_conditions']})
    tdicprsar.update({'TestLSQ':tdicprsar['names_of_locations']})    
    names_of_conditions_list = []
    for item in tdicprsar['names_of_conditions']:
        names_of_conditions_list.append(CONDITIONS_DICT[item])
    tdicprsar.update({'TestNCL':names_of_conditions_list})
    df_mean = pandas.DataFrame(index=tdicprsar['names_of_locations'], columns=names_of_conditions_list)
    
    i = 0
    for location in tdicprsar['names_of_locations']:
        j = 0
        for condition in names_of_conditions_list: 
            # строки, у которых значение в conditions = condition & значение в locations = location
            ttt = result_DF.loc[((result_DF['conditions']==tdicprsar['names_of_conditions'][j]) & (result_DF['location']==tdicprsar['names_of_locations'][i]))]['_value'].mean()
            df_mean.loc[location, condition] = ttt
            j = j + 1
        i = i + 1

    df_mean_ri = df_mean.reindex(columns=NAME_COL_LIST)
    tdicprsar.update({'result_df_mean':df_mean_ri.to_html()})  # Таблица html
    tdicprsar.update({'result_points_JS':df_mean_ri.T.to_json})    # Транспонированный DataFrame -> json
    return render(request, 'personalarea/work_with_points.html', context=tdicprsar)

def testing(request):

    # Запись тестовой последовательности в БД InfluxDB

    if request.method == "POST":
        form = NumberOfPoints(request.POST)
        if form.is_valid():
            tdicprsar.update({'measurement':'hr_measurement'})
            tdicprsar.update({'location':form.cleaned_data.get('location')})
            tdicprsar.update({'conditions':form.cleaned_data.get('conditions')})
            tdicprsar.update({'number_of_points_write':form.cleaned_data.get('number_of_points')}) 
            write_influxDB()
            points_list = []
            read_influxDB(points_list)
            logged_out_view()
    else:
            form = NumberOfPoints()
    tdicprsar.update({'form':form})
    return render(request, 'personalarea/testing.html', context=tdicprsar)
	
def grouphr_create(request):

    # Добавление группы пользователей руководителем

    tdicprsar.update({'TestGC':'grouphr_create'})
    form = RegistrationGrouphr(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
    context = {'form': form}
    html_form = render_to_string('includes/partial_grouphr_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})

def turn_on(request):

    return render(request, 'personalarea/templates/prsar.html', context=tdicprsar)
	
def turn_off(request):

    return render(request, 'personalarea/prsar.html', context=tdicprsar)