
from django.template import Template, Context, loader
from django.shortcuts import render, redirect
from django.http import HttpResponse



def home(request):
    # Create Template Object
   # template = loader.get_template('home.html')
   # context = { 'home_url' : 'http://127.0.0.1:8002/' }
    return render(request, 'home.html')

