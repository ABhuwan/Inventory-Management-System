from django.http import HttpResponse
from django.shortcuts import render

def aboutus(request):
    return HttpResponse("<h1>heading</h2>")

def home(request):
    return render(request, 'homepage.html')