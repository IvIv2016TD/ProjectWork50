from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
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
    ('1', 'Выключить/включить старую группу'),
    ('2', 'Выключить/включить пользователя'),
]

WORKS_LIVE_DICT = {
    '0':'Зарегистрировать новую группу',
    '1':'Выключить/включить старую группу',
    '2':'Выключить/включить пользователя',
}

def prsar_view(request):
    
    global tdicprsar
    
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

    if request.POST:
        form = WorksForm(request.POST)
        if form.is_valid():
            #tdicprsar.update({'test_POST':'conditionsV'})
            works_live = form.cleaned_data.get('works_live')
            #tdicprsar.update({'works_live_str':WORKS_LIVE_DICT[works_live]})
            tdicprsar.update({'works_live':works_live})
            if works_live == '0':
                tdicprsar.update({'works_live_test':works_live})
                tdicprsar.update({'TestGC':'prsar_view'})
                form_0 = RegistrationGrouphr(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
                tdicprsar.update({'form_0':form_0})
                return render(request, 'personalarea/prsar_reggr.html', context=tdicprsar)
                #tl_groups = Groupshr.objects.filter(user=user)
                #n_grouphr = tl_groups.values_list('name_of_grouphr', 'time_of_registration', 'comment_of_TL', 'operating_grouphr')
                #tdicprsar.update({'n_grouphr':n_grouphr})                
                #return redirect('prsar_reggr.html')
                #prsar_reggr_view(request)
                #return render(request, 'prsar_reggr.html', context=tdicprsar)
                #if request.POST:
                #    form_0 = RegistrationGroupHR(request.POST, username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
                #    if form_0.is_valid():
                #        #tdicprsar.update({'test_POST':'conditionsV'})
                #        name_of_grouphr = form_0.cleaned_data.get('name_of_grouphr')
                #        comment_of_TL = form_0.cleaned_data.get('comment_of_TL')
                #        tdicprsar.update({'name_of_grouphr':name_of_grouphr})
                #        tdicprsar.update({'comment_of_TL':comment_of_TL})
                #        return render(request, 'prsar_reggr.html', context=tdicprsar)
                #        #return HttpResponseRedirect('http://yandex.ru/')
                #else:
                #    form_0 = RegistrationGroupHR(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
                #    #tdicprsar.update({'test_POST':'conditionsW'})
                #tdicprsar.update({'form_0':form_0})
                #tdicprsar.update({'prsar_reggr_view':'prsar_reggr_view'})
                ##return render(request, 'prsar_reggr.html', context=tdicprsar)
                ##return HttpResponseRedirect('http://yandex.ru/')				
    else:
        form = WorksForm()
        works_live = "-1"
        #tdicprsar.update({'test_POST':'conditionsW'})
    tdicprsar.update({'form':form})
    tdicprsar.update({'WORKS_LIVE':WORKS_LIVE})

    #if works_live == '0':
    #    if request.POST:
    #        form_0 = RegistrationGroupHR(request.POST, username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
    #        if form_0.is_valid():
    #            #tdicprsar.update({'test_POST':'conditionsV'})
    #            name_of_grouphr = form_0.cleaned_data.get('name_of_grouphr')
    #            comment_of_TL = form_0.cleaned_data.get('comment_of_TL')
    #            tdicprsar.update({'name_of_grouphr':name_of_grouphr})
    #            tdicprsar.update({'comment_of_TL':comment_of_TL})
    #    else:
    #        form_0 = RegistrationGroupHR(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
    #        #tdicprsar.update({'test_POST':'conditionsW'})
    #    tdicprsar.update({'form_0':form_0})

	
    #elif works_live == 1:
        
    #elif works_live == 2:		

    return render(request, 'prsar.html', context=tdicprsar)

def prsar_reggr_view(request):
    tdicprsar.update({'TestGC':'prsar_reggr_view'})
    tdicprsar.update({'TestPRV':prv})

    if request.POST:
        #form_0 = RegistrationGrouphr(request.POST, username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
        if tdicprsar['form_0'].is_valid():
            #tdicprsar.update({'test_POST':'conditionsV'})
            name_of_grouphr = form_0.cleaned_data.get('name_of_grouphr')
            comment_of_TL = form_0.cleaned_data.get('comment_of_TL')
            tdicprsar.update({'name_of_grouphr':name_of_grouphr})
            tdicprsar.update({'comment_of_TL':comment_of_TL})
    else:
        form_0 = RegistrationGrouphr(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
       #tdicprsar.update({'test_POST':'conditionsW'})
    tdicprsar.update({'form_0':form_0})

    return render(request, 'prsar_reggr.html', context=tdicprsar)
	
def logged_out_view(request):

    seanse = Seanses.create_seanse(request.user.username, tdicprsar['time_of_begin'],
                tdicprsar['number_of_points_write'], tdicprsar['number_of_points_read'])	
    seanse.save()
    logout(request)	
    return render(request, 'logged_out.html', context=tdicprsar)

def write_influxDB():
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    import random

#    bucket = "HRWEB"
#    org = "PM72"
#    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
## Store the URL of your InfluxDB instance
#
#    url="https://eu-central-1-1.aws.cloud2.influxdata.com/"

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    npoints = tdicprsar['number_of_points_write'] 
    tdicprsar.update({'hr_measurement':MEASUREMENT})
    min = -5
    max = 15
    for item in range(tdicprsar['number_of_points_write']):
        hr = 70 + random.randint(min, max)
        p = influxdb_client.Point(tdicprsar['hr_measurement']).tag("username", tdicprsar['username']).tag("location", tdicprsar['location']).tag("conditions", tdicprsar['conditions']).field("hr_per_minute", hr)
        write_api.write(bucket=BUCKET, org=ORG, record=p)	

def read_influxDB(points_list):
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

#    bucket = "HRWEB"
#    org = "PM72"
#    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
## Store the URL of your InfluxDB instance
#
#    url="https://eu-central-1-1.aws.cloud2.influxdata.com/"

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    query_api = client.query_api()
    username = '"' + tdicprsar['username'] + '"'
    bucket = '"' + BUCKET + '"'
    measurement = '"' + MEASUREMENT + '"'
    #query = 'from(bucket:"HRWEB")\
    #|> range(start: -10m)\
    #|> filter(fn:(r) => r._measurement == "hr_measurement")\
    #|> filter(fn:(r) => r.username == "TestUser2")\
    #|> filter(fn:(r) => r.location == "Новосибирск")\
    #|> filter(fn:(r) => r._field == "hr_per_minute" )'

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
	
    return #points_list

def read_influxDB_params(points_list, *args, **params_dict):
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

#    bucket = "HRWEB"
#    org = "PM72"
#    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
## Store the URL of your InfluxDB instance
#
#    url="https://eu-central-1-1.aws.cloud2.influxdata.com/"

    client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
    query_api = client.query_api()
    username = '"' + tdicprsar['username'] + '"'
    bucket = '"' + BUCKET + '"'
    measurement = '"' + MEASUREMENT + '"'
    start_datatime = str(int((params_dict['time_of_begin'] - params_dict['delta_param']).timestamp()))
    end_datatime = str(int((params_dict['time_of_end']).timestamp()))
    tdicprsar.update({'TestS':start_datatime})
    tdicprsar.update({'TestE':end_datatime})
    #query = 'from(bucket:"HRWEB")\
    #|> range(start: -10m)\
    #|> filter(fn:(r) => r._measurement == "hr_measurement")\
    #|> filter(fn:(r) => r.username == "TestUser2")\
    #|> filter(fn:(r) => r.location == "Новосибирск")\
    #|> filter(fn:(r) => r._field == "hr_per_minute" )'

    #query = 'from(bucket:' + bucket + ')\
    #|> range(start: ' + start_datatime + ', stop: ' + end_datatime + ')\
    query0 = 'from(bucket:"HRWEB")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == ' + measurement + ')\
    |> filter(fn:(r) => r.username == ' + username + ')\
    |> filter(fn:(r) => r.location == "Новосибирск")\
    |> filter(fn:(r) => r._field == "hr_per_minute" )'

    query = 'from(bucket:' + bucket + ')\
    |> range(start: ' + start_datatime + ', stop: ' + end_datatime + ')\
    |> filter(fn:(r) => r._measurement == ' + measurement + ')'#\
    #|> filter(fn:(r) => r.username == ' + username + ')\
    #|> filter(fn:(r) => r.location == "Новосибирск")\
    #|> filter(fn:(r) => r._field == "hr_per_minute" )'

    query2 = 'from(bucket:' + bucket + ')\
    |> range(start: 1623498412, stop: 1623498487)\
    |> filter(fn:(r) => r._measurement == ' + measurement + ')\
    |> filter(fn:(r) => r.username == ' + username + ')\
    |> filter(fn:(r) => r.location == "Новосибирск")\
    |> filter(fn:(r) => r._field == "hr_per_minute" )'	
    tdicprsar.update({'TestA':query})

    result = client.query_api().query(org=ORG, query=query)
    tdicprsar.update({'TestRR':len(result)})

    results = []
    for table in result:
        for record in table.records:
            results.append((record.values.get('location'), record.values.get('username'), record.values.get('conditions'), record.get_time(), record.get_field(), record.get_value()))

    tdicprsar.update({'TestRT':len(results)})
    #tdicprsar.update({'TestTK':schema.tagKeys(bucket: "HRWEB")})

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
    #names_of_user.append("TestUser9")
    #names_of_user.append("TestUser1")
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
    #result = []
    tdicprsar.update({'TestRR':len(result)})

    #results = []
    #for table in result:
    #    for record in table.records:
    #        results.append((record.values.get('location'), record.values.get('username'), record.values.get('conditions'), #record.get_time(), record.get_field(), record.get_value()))

    #tdicprsar.update({'TestRT':len(results)})
    ##tdicprsar.update({'TestTK':schema.tagKeys(bucket: "HRWEB")})

    delta = timedelta(hours=7, minutes=0)
    #for item in results:

    #    points_list.append("Место " + str(item[0]) + "Имя пользователя " + str(item[1]) + "Условия " + str(item[2]) +
#		  " Дата, время" + (item[3] + delta).strftime('%d/%m/%Y, %H:%M:%S') +
#          " Имя поля " + str(item[4]) +
#          " Значение " + str(item[5])
#          )

#    tdicprsar.update({'number_of_points_read':len(results)})
#    tdicprsar.update({'points_list':points_list})
#    tdicprsar.update({'results':results})
    tdicprsar.update({'result':result.to_html()})	
	
    return
	
def work_with_seanses(request):

    if request.POST:
        form = UsersSeanses(request.POST, username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
        if form.is_valid():
            #birth_year = form.cleaned_data.get('birth_year')
            #seanses_of_user = form.cleaned_data.get('seanses_of_user')
            #conditions = form.cleaned_data.get('conditions')
            #location = form.cleaned_data.get('location')
            tdicprsar.update({'test_POST':'conditionsV'})
            #tdicprsar.update({'seanses_of_user':seanses_of_user})
            #tdicprsar.update({'location':conditions})
            seanses_of_user = form.cleaned_data.get('seanses_of_user')
            #location = form.cleaned_data.get('location')
            tdicprsar.update({'seanses_of_user':seanses_of_user})
    else:
        form = UsersSeanses(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
        tdicprsar.update({'test_POST':'conditionsW'})
    tdicprsar.update({'form':form})    
    return render(request, 'personalarea/work_with_seanses.html', context=tdicprsar)

def work_with_series(request):
    
    user_seanses = Seanses.objects.filter(id__in=tdicprsar['seanses_of_user']).values_list('id', 'time_of_begin', 'time_of_end', 'number_of_points_write', 'number_of_points_read')
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

    ttt = []
    ttt.append("ttt1")
    ttt.append("ttt2")
    tdicprsar.update({'ttt':ttt})
    tdicprsar.update({'TestUN':len(ttt)})
    #tdicprsar.update({'list_username':ttt})

    #args_tuple = 0
    #query_params_dict = {}
    #query_params_dict.update({'names':tdicprsar['list_username']})
    #query_params_dict.update({'locations':tdicprsar['list_location']})
    #query_params_dict.update({'conditions':tdicprsar['list_conditions']})	
    #names=tdicprsar['list_username']
    #locations=tdicprsar['list_location']
    #conditions=tdicprsar['list_conditions']
    if request.POST:
        form = UsersPoints(request.POST, locations=tdicprsar['list_location'], conditions=tdicprsar['list_conditions'], username=tdicprsar['list_username'])
        if form.is_valid():
            #tdicprsar.update({'test_POST':'conditionsV'})
            names_of_user = form.cleaned_data.get('names_of_user')
            names_of_locations = form.cleaned_data.get('names_of_locations')
            names_of_conditions= form.cleaned_data.get('names_of_conditions')
            #tdicprsar.update({'seanses_of_user':seanses_of_user})
# читаем из InfluxDB DataFrame со всеми выбранными сериями
            params_dict.update({'names_of_user':names_of_user})
            params_dict.update({'names_of_locations':names_of_locations})
            params_dict.update({'names_of_conditions':names_of_conditions})			
            read_influxDB_DataFrame(points_list, *args, **params_dict)	
    else:
        form = UsersPoints(locations=tdicprsar['list_location'], conditions=tdicprsar['list_conditions'], username=tdicprsar['list_username'])
        #tdicprsar.update({'test_POST':'conditionsW'})
    tdicprsar.update({'form':form})
	
    return render(request, 'personalarea/work_with_series.html', context=tdicprsar)

def work_with_points(request):
    return render(request, 'personalarea/work_with_points.html', {})

def testing(request):

    if request.method == "POST":
        form = NumberOfPoints(request.POST)
        if form.is_valid():
#            number_of_points_write = form.cleaned_data.get('number_of_points')
#            tdicprsar.update({'number_of_points_write':number_of_points_write})
            tdicprsar.update({'measurement':'hr_measurement'})
            tdicprsar.update({'location':form.cleaned_data.get('location')})
            tdicprsar.update({'conditions':form.cleaned_data.get('conditions')})
            tdicprsar.update({'number_of_points_write':form.cleaned_data.get('number_of_points')}) 
            write_influxDB()
            points_list = []
            read_influxDB(points_list)
            #points_list = []
            #points_list.append('Точка 1')
            #tdicprsar.update({'points_list':points_list})
    else:
            form = NumberOfPoints()
    tdicprsar.update({'form':form})
    return render(request, 'personalarea/testing.html', context=tdicprsar)
	
def grouphr_create(request):
    tdicprsar.update({'TestGC':'grouphr_create'})
    form = RegistrationGrouphr(username=tdicprsar['username'], tb=tdicprsar['time_of_begin'])
    context = {'form': form}
    html_form = render_to_string('includes/partial_grouphr_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})