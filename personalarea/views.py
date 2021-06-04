from django.shortcuts import render
from django.contrib.auth import logout
from accounts.models import Profile, Seanses
from datetime import datetime

from .forms import NumberOfPoints

# Create your views here.

def prsar_view(request):
    
    global tdicprsar
    
    user = request.user.username
    tdicprsar = {'username':user}
    user_seanses = Seanses.objects.filter(user=user)
    num_seanses = len(user_seanses)
    tdicprsar.update({'num_seanses':num_seanses})
    time_of_last_visit = user_seanses.values_list('time_of_begin', flat=True).last()
    tdicprsar.update({'time_of_last_visit':time_of_last_visit})
    tdicprsar.update({'time_of_begin':datetime.now()})

    number_of_points_write = 0
    tdicprsar.update({'number_of_points_write':number_of_points_write})
    if request.method == "POST":
        form = NumberOfPoints(request.POST)
        if form.is_valid():
            number_of_points_write = form.cleaned_data.get('number_of_points')
            tdicprsar.update({'number_of_points_write':number_of_points_write})
            write_influxDB(number_of_points_write)
    else:
            form = NumberOfPoints()
    tdicprsar.update({'form':form})
    number_of_points_read = 0
    tdicprsar.update({'number_of_points_read':number_of_points_read})	
    return render(request, 'prsar.html', context=tdicprsar)
	
def logged_out_view(request):

    seanse = Seanses.create_seanse(request.user.username, tdicprsar['time_of_begin'],
                tdicprsar['number_of_points_write'], tdicprsar['number_of_points_read'])	
    seanse.save()
    logout(request)	
    return render(request, 'logged_out.html', context=tdicprsar)

def write_influxDB(npoints):
    import influxdb_client
    from influxdb_client.client.write_api import SYNCHRONOUS

    import random

    bucket = "HRWEB"
    org = "PM72"
    token = "3sLsq9ECi2eSQEYQQjIdxZsTuV6NtFcaohVKzNeILEo5hOPGCRt0Mmgzug_8iai9fCNfbUD1s3wAYd5LAXHOjg=="
# Store the URL of your InfluxDB instance

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

    return results