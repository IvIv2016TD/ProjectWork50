from django.shortcuts import render

# Create your views here.

def prsar_view(request):
    tdicprsar = {'prsar':request.user.username}
    return render(request, 'prsar.html', context=tdicprsar)