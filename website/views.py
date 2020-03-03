
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.conf.urls import include, url
from website import views
from django.core.files.storage import FileSystemStorage
import pandas as pd
from apyori import apriori
import os
from os.path import dirname, abspath


def algorithm(request):
    return render(request, 'website/algorithm.html')


def calculate(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_name']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)

        minsupp = request.POST['minsupp']
        minconf = request.POST['minconf']
        selectedAlgorithm = request.POST['selectedAlgorithm']

        BASE_DIR = dirname(os.path.dirname(os.path.abspath(__file__)))
        url_split = url.split("/")
        for value in url_split:
            if value == '':
                url_split.remove(value)
        for value in url_split:
            BASE_DIR = BASE_DIR + "\\" + str(value)

        store_data = pd.read_csv(BASE_DIR, header=None)

        records = []
        for i in range(0, len(store_data)):
            records.append([str(store_data.values[i, j])
                            for j in range(0, 20)])
        records_withoutNan = []

        for i in range(0, len(records)):
            new = []
            for j in range(0, len(records[i])):
                if str(records[i][j]) != "nan":
                    new.append(str(records[i][j]))
            records_withoutNan.append(new)
        # print(records_withoutNan)

        if selectedAlgorithm == 'Apriori':
            association_rules = apriori(records_withoutNan, min_support=(
                float(minsupp)/100), min_confidence=float(minconf))
            association_results = list(association_rules)
        print("Number Rules: "+ str(len(association_results)))
        association_results_final = []
        
        for item in association_results:
            one_rule = {}
            one_rule['dad'] = list(item[2][0][0])
            one_rule['sup'] = list(item[2][0][1])
            one_rule['minsupp'] = item[1]
            one_rule['minconf'] = item[2][0][2]
            association_results_final.append(one_rule)
        
        # print(association_results_final)
        
    return render(request, 'website/show_rules.html', {'association_rules': association_results_final})
