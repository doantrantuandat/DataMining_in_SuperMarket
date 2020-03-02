
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf.urls import include, url
from website import views


def algorithm(request):
    return render(request, 'website/algorithm.html')


def calculate(request):
    if request.method == 'POST':
        fileName = request.POST['txtFile']
        selectedAlgorithm = request.POST['selectedAlgorithm']
        minsupp = request.POST['minsupp']
        minconf = request.POST['minconf']
    return render(request, 'website/show_rules.html', {'fileName': fileName, 'minsupp': minsupp, 'selectedAlgorithm': selectedAlgorithm, 'minconf': minconf})
