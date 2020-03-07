
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf.urls import include, url
from website import views
from django.core.files.storage import FileSystemStorage
import pandas as pd
from apyori import apriori
import os
from os.path import dirname, abspath
import pyfpgrowth


def algorithm(request):
    return render(request, 'website/algorithm.html')


def calculate(request):
    if request.method == 'POST':
        """
        Get data inject from html
        """
        # upload and get file
        uploaded_file = request.FILES['file_name']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)

        url = fs.url(name)
        # get minsupp and minconf
        minsupp = request.POST['minsupp']
        minconf = request.POST['minconf']
        # get algorithm
        selectedAlgorithm = request.POST['selectedAlgorithm']

        BASE_DIR = dirname(os.path.dirname(os.path.abspath(__file__)))
        url_split = url.split("/")
        for value in url_split:
            if value == '':
                url_split.remove(value)
        for value in url_split:
            BASE_DIR = BASE_DIR + "\\" + str(value)
        # read dataset
        if name.find(".csv") != -1:
            store_data = pd.read_csv(BASE_DIR, header=None)
        if name.find(".xlsx") != -1:
            store_data = pd.read_excel(BASE_DIR, header=None)
        # change data conform algorithm
        records = []
        for i in range(0, len(store_data)):

            records.append([str(store_data.values[i, j])
                            for j in range(0, len(store_data.columns))])

        records_withoutNan = []

        for i in range(0, len(records)):
            new = []
            for j in range(0, len(records[i])):
                if str(records[i][j]) != "nan":
                    new.append(str(records[i][j]))
            records_withoutNan.append(new)
        """
        function FP-GROWTH algorithm
        return pattens, rules
        in rules have (super rules, sup rules and confidence every a rules)
        """
        def fpgrowth_find_association_rules(dataset, minsup, minconf):
            patterns = pyfpgrowth.find_frequent_patterns(
                dataset, float(minsup)/100*len(dataset))
            rules = pyfpgrowth.generate_association_rules(
                patterns, float(minconf))
            return patterns, rules
        """
        function APRIORI algorithm
        return alist rules
        in rules have (super rules, sup rules and confidence every a rules)
        """
        def apriori_find_association_rules(dataset, minsup, minconf):
            association_rules = apriori(records_withoutNan, min_support=(
                float(minsupp)/100), min_confidence=float(minconf))
            association_results = list(association_rules)
            return association_results
        """
        set event use Apriori or FP_Growth
        """
        if selectedAlgorithm == 'Apriori':
            """
            association_results_APRIORI: is a List Object Apriori return after calculate
            """
            association_results_APRIORI = apriori_find_association_rules(
                records_withoutNan, minsupp, minconf)
            # Get rules have confidence max
            # return a list max value of object rules
            for item in association_results_APRIORI:
                print(item[2])
            association_results_final_apriori = []
            max_conf_arr = []
            for item in association_results_APRIORI:
                max_conf = 0
                for i in range(0, len(item[2])):
                    if item[2][i][2] > max_conf:
                        max_conf = item[2][i][2]
                max_conf_arr.append(max_conf)
            association_results_APRIORI_temp = []
            # comparing max and values in association_results_APRIORI
            for i in range(0, len(association_results_APRIORI)):
                for j in range(0, len(association_results_APRIORI[i][2])):
                    if association_results_APRIORI[i][2][j][2] == max_conf_arr[i]:
                        association_results_APRIORI_temp.append(association_results_APRIORI[i][2][j])
            # assign value type allow json form
            for item in association_results_APRIORI_temp:
                one_rule = {}
                one_rule['dad'] = list(item[0])
                one_rule['sup'] = list(item[1])
                one_rule['minconf'] = round(item[2], 3)
                association_results_final_apriori.append(one_rule)

            return render(request, 'website/show_rules.html', {'selectedAlgorithm': selectedAlgorithm, 'lenrules': len(association_results_final_apriori), 'lendata': len(records_withoutNan), 'association_rules': association_results_final_apriori})
        elif selectedAlgorithm == 'FP-Growth':
            association_results_FPGROWTH_patterns, association_results_FPGROWTH_rules = fpgrowth_find_association_rules(
                records_withoutNan, minsupp, minconf)
            association_results_final_fpgrowth = []
            for key, val in association_results_FPGROWTH_rules.items():
                one_rule = {}
                one_rule['dad'] = key
                one_rule['sup'] = val[0]
                one_rule['minconf'] = round(val[1], 3)
                if len(one_rule['sup']) == 0:
                    continue

                association_results_final_fpgrowth.append(one_rule)
            return render(request, 'website/show_rules.html', {'selectedAlgorithm': selectedAlgorithm, 'lenrules': len(association_results_final_fpgrowth), 'lendata': len(records_withoutNan), 'association_rules': association_results_final_fpgrowth})
