from django.shortcuts import render, redirect, loader
from django.http import HttpResponse
from programLocation.bridge import search_initialize

# Create your views here.
def scavenger(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def search_term(request):
    result = search_initialize()
    return render(request, 'websiteDjango\scavenger\templates\home.html', {'result': result})
