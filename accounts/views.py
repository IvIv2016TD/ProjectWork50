# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUpForm
from django.urls import reverse_lazy
from django.views import generic
from django.http  import  HttpResponse
import datetime

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

import smtplib

from .forms import SignUpForm, NumberOfPoints
from .tokens import account_activation_token

def home(request):
    return render(request, 'accounts/home.html', {})
	
def test_IDB(request):
    if request.method == "POST":
        form = NumberOfPoints(request.POST)
        if form.is_valid():
            number_of_points = form.cleaned_data.get('number_of_points')
            write_influxDB(number_of_points)
#            data_InfluxDB = 'Точки тестовой последовательности InfluxDB'
#            results = []
#            results = read_influxDB()
#            one = open("One.txt", 'a')
#            index = 0
#            for item in results:
#              one.write(str(index)+ "   " + str((results[index])) + "\n")
#              index = index + 1
#            one.write(str(1000) + "\n")
#            one.flush()
#            one.close()
    else:
            #return redirect('home')
            #return HttpResponse(u'Куда прёшь?')
            form = NumberOfPoints()
    #return redirect('home')
    #return HttpResponse(u'Не туда прёшь!')	
    return render(request, 'accounts/test_IDB.html', {'form':form})

def write_influxDB(npoints):
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    import random

    bucket = "HRWEB"
    org = "PM72"
    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
# Store the URL of your InfluxDB instance
#url="http://localhost:8086"
    url="https://eu-central-1-1.aws.cloud2.influxdata.com/"

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    write_api = client.write_api(write_options=SYNCHRONOUS)

    #npoints = 1000
    min = -5
    max = 15
    for item in range(npoints):
        hr = 70 + random.randint(min, max)
        p = influxdb_client.Point("my_measurement_1").tag("location", "Novosibirsk").field("hr_per_minute", hr)
        write_api.write(bucket=bucket, org=org, record=p)	

def read_influxDB():
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    bucket = "HRWEB"
    org = "PM72"
    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
# Store the URL of your InfluxDB instance
#url="http://localhost:8086"
    url="https://eu-central-1-1.aws.cloud2.influxdata.com/"

    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
    query_api = client.query_api()
    query = 'from(bucket:"HRWEB")\
    |> range(start: -10m)\
    |> filter(fn:(r) => r._measurement == "my_measurement_1")\
    |> filter(fn: (r) => r.location == "Novosibirsk")\
    |> filter(fn:(r) => r._field == "hr_per_minute" )'
    result = client.query_api().query(org=org, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))
#    one = open("One.txt", 'a')
#    index = 0
#    for item in results:
#        one.write(str(index)+ "   " + str((results[index])) + "\n")
#        index = index + 1
#    one.write(str(1000) + "\n")
#    one.flush()
#    one.close()
    return results
	
	
def about_test(request):
    test_IDB_1(3)
	#console.log('Привет')
	#print("test_IDB_1")
    #return  HttpResponse ('Тест about')
    #return render(request, 'accounts/about_test.html', {})
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)	
	
#def test_IDB_1(request):
#    numpoints = request.POST[number_of_points]
	#return  HttpResponse ('Тест test_IDB')
	#print(numpoints)
 
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('index')
    template_name = 'signup.html'

def home_view(request):
    return render(request, 'home.html')

def activation_sent_view(request):
    return render(request, 'activation_sent.html')
	
def activation_invalid_view(request):
    return render(request, 'activation_invalid.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # проверка того, что пользователь существует и токен его валиден
    if user is not None and account_activation_token.check_token(user, token):
        # если да - активируем аккаунт 
        user.is_active = True
        # установка флага подтверждения регистрации
        user.profile.signup_confirmation = True
        user.save()
		# присоединение пользователя к текущему сеансу
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # пользователь не сможет залогинится пока регистрация не будет подтверждена
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Пожалуйста, активируйте свой аккаунт'
            # загружаем и заполняем шаблон 
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # метод вычисляет хэш по данным нового пользователя
                'token': account_activation_token.make_token(user),
            })
            msg = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [user.profile.email])         
            msg.attach_alternative(message, "text/html")
            msg.send()
            return redirect('activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})	
