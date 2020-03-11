
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
from numpy import array_equal
from django import template
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules
from mlxtend.frequent_patterns import fpgrowth, apriori


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
        
        te = TransactionEncoder()
        te_ary = te.fit(records_withoutNan).transform(records_withoutNan)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        """
        function APRIORI algorithm
        return alist rules
        in rules have (super rules, sup rules and confidence every a rules)
        """
        def apriori_find_association_rules(dataset, minsup, minconf):
            patterns_ap = apriori(df, min_support=float(minsupp)/100, use_colnames=True)
            rules_ap = association_rules(patterns_ap, metric="confidence", min_threshold=float(minconf)/100)
            rules_ap_sort_descending = rules_ap.sort_values(by="confidence", ascending=False)
            return rules_ap_sort_descending
        """
        function FP-GROWTH algorithm
        return pattens, rules
        in rules have (super rules, sup rules and confidence every a rules)
        """
        def fpgrowth_find_association_rules(dataset, minsup, minconf):
            patterns_fp = fpgrowth(df, min_support=float(minsupp)/100, use_colnames=True, verbose=0)
            rules_fp = association_rules(patterns_fp, metric="confidence", min_threshold=float(minconf)/100)
            rules_fp_sort_descending = rules_fp.sort_values(by="confidence", ascending=False)
            return rules_fp_sort_descending

        """
        set event use Apriori or FP_Growth
        """
        if selectedAlgorithm == 'Apriori':
            """
            association_results_APRIORI: is a List Object Apriori return after calculate
            """
            association_results_APRIORI = apriori_find_association_rules(
                df, minsupp, minconf)
            rules_ap_antecedents_list = list(association_results_APRIORI['antecedents'])
            rules_ap_consequents_list = list(association_results_APRIORI['consequents'])
            rules_ap_support_list = list(association_results_APRIORI['support'])
            rules_ap_confidence_list = list(association_results_APRIORI['confidence'])
            rules_ap_lift_list = list(association_results_APRIORI['lift'])

            rules_ap_final = []
            for i in range(0, len(rules_ap_antecedents_list)):
                onerules = {}
                onerules['antecedents'] = list(rules_ap_antecedents_list[i])
                onerules['consequents'] = list(rules_ap_consequents_list[i])
                onerules['support'] = round(rules_ap_support_list[i], 3)
                onerules['confidence'] = round(rules_ap_confidence_list[i], 3)
                onerules['lift'] = round(rules_ap_lift_list[i], 3)
                rules_ap_final.append(onerules)
            

            return render(request, 'website/show_rules.html', {'selectedAlgorithm': selectedAlgorithm, 'lenrules': len(rules_ap_final), 'lendata': len(df), 'association_rules': rules_ap_final})
        elif selectedAlgorithm == 'FP-Growth':
            
            
            association_results_FPGROWTH = fpgrowth_find_association_rules(
                df, minsupp, minconf)
            
            rules_fp_antecedents_list = list(association_results_FPGROWTH['antecedents'])
            rules_fp_consequents_list = list(association_results_FPGROWTH['consequents'])
            rules_fp_support_list = list(association_results_FPGROWTH['support'])
            rules_fp_confidence_list = list(association_results_FPGROWTH['confidence'])
            rules_fp_lift_list = list(association_results_FPGROWTH['lift'])
            
            rules_fp_final = []
            for i in range(0, len(rules_fp_antecedents_list)):
                onerules = {}
                onerules['antecedents'] = list(rules_fp_antecedents_list[i])
                onerules['consequents'] = list(rules_fp_consequents_list[i])
                onerules['support'] = round(rules_fp_support_list[i], 3)
                onerules['confidence'] = round(rules_fp_confidence_list[i], 3)
                onerules['lift'] = round(rules_fp_lift_list[i], 3)
                rules_fp_final.append(onerules)
            return render(request, 'website/show_rules.html', {'selectedAlgorithm': selectedAlgorithm, 'lenrules': len(rules_fp_final), 'lendata': len(df), 'association_rules': rules_fp_final})
