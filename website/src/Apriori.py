import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from apyori import apriori
import os
from os.path import dirname, abspath

BASE_DIR = dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
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

association_rules = apriori(
    records_withoutNan, min_support=float(250/7500), min_confidence=0.2)
association_results = list(association_rules)


print("=============================================")
print("Number association rules: " + str(len(association_results)))

for item in association_results:
    print("=====================================")
    print("Rule: " + str(list(item[2][0][0])) +
          " -> " + str(list(item[2][0][1])))
    print("Support: " + str(item[1]))
    print("Confidence: " + str(item[2][0][2]))
    print("Lift: " + str(item[2][0][3]))
print("=============================================")
print("Number association rules: " + str(len(association_results)))
