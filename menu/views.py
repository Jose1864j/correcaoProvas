from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def redirectStart(request):
    return redirect('/menu/iniciar/')

def start(request):
    return render(request, 'start.html')
def selecionar(request, url):
    return redirect(url)