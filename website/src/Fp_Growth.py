import pyfpgrowth
import pandas as pd
import numpy as np
import os
from os.path import dirname, abspath

BASE_DIR = dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(str(BASE_DIR), "data\store_data.csv")
store_data = pd.read_csv(path, header=None)


records = []
for i in range(0, 7501):
    records.append([str(store_data.values[i, j]) for j in range(0, 20)])

records_withoutNan = []
for i in range(0, len(records)):
    new = []
    for j in range(0, len(records[i])):
        if str(records[i][j]) != "nan":
            new.append(str(records[i][j]))
    records_withoutNan.append(new)


def fp_find_association_rules(dataset, minsup, minconf):
    patterns = pyfpgrowth.find_frequent_patterns(dataset, minsup)
    rules = pyfpgrowth.generate_association_rules(patterns, minconf)
    return patterns, rules


def fp_show_mining_results(patterns, rules):

    print("Rules:\n------")
    c = 0
    for key, val in rules.items():
        head = key
        tail = val[0]
        confidence = val[1]
        if len(tail) == 0:
            continue
        print('({}) ==> ({})  confidence = {}'.format(
            ', '.join(head), ', '.join(tail), round(confidence, 3)))
        c += 1
    print("================================================")
    print("Number Rules: " + str(c))


if __name__ == '__main__':
    patterns, rules = fp_find_association_rules(records_withoutNan, 250, 0.2)
    fp_show_mining_results(patterns, rules)
