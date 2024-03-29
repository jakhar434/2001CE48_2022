# import pandas as pd
# file = pd.read_csv (r'octant_list_output.csv')
# print("sum of octant_list_list is ", file['octant_list_list'].sum());
from datetime import datetime
start_time = datetime.now()

from itertools import count
import numpy as np
import math
from multiprocessing.sharedctypes import Value
import pandas as pd


#change the value of mod here
mod = 5000


file = pd.read_excel("input_octant_longest_subsequence.xlsx")
# finding the average value of U, V AND W
average_u = file['U'].mean()
average_v = file['V'].mean()
average_w = file['W'].mean()
# adding this to csv file
# print(len(file))
file.at[0, "U Avg"] = average_u
file.at[0, "V Avg"] = average_v
file.at[0, "W Avg"] = average_w
# subtarcting the value from average values and adding to csv file

file["U'=U - U avg"] = file['U']-average_u
file["V'=V - V avg"] = file['V']-average_v
file["W'=W - W avg"] = file['W']-average_w

# +ve, +ve 1st quadrant
# -ve , +ve 2nd quadrant
# -ve, -ve 3rd quadrant
# +ve, -ve 4th quadrant
octant_list_list = []
for x in range(len(file)):

    if (file["U'=U - U avg"][x] > 0 and file["V'=V - V avg"][x] > 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list_list.append(1)
        else:
            octant_list_list.append(-1)

    elif (file["U'=U - U avg"][x] < 0 and file["V'=V - V avg"][x] > 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list_list.append(2)
        else:
            octant_list_list.append(-2)

    elif (file["U'=U - U avg"][x] < 0 and file["V'=V - V avg"][x] < 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list_list.append(3)
        else:
            octant_list_list.append(-3)

    else:
        if (file["W'=W - W avg"][x] >= 0):
            octant_list_list.append(4)
        else:
            octant_list_list.append(-4)

file["octant"] = octant_list_list
# dictionary is formed and calculate longest subsequence length
dictionary_count = {1: 0, -1: 0, 2: 0, -2: 0, 3: 0, -3: 0, 4: 0, -4: 0}     

for z in range(-4, 5):
    if (z == 0):
        continue
    flag = 0                                          
    for j in range(len(file)-1):
        if (file.at[j, "octant"] == file.at[j+1, "octant"] and file.at[j, "octant"] == z):
            flag += 1
        else:
            dictionary_count[z] = max(dictionary_count[z], flag+1)
            flag = 0
## now we have to calculate frequency
dict_count = {1: 0, -1: 0, 2: 0, -2: 0, 3: 0, -3: 0, 4: 0, -4: 0}

for i in range(-4, 5):
    if (i == 0):
        continue
    flag = 0
    for j in range(len(file)-1):
        if (file.at[j, "octant"] == file.at[j+1, "octant"] and file.at[j, "octant"] == i):
            flag += 1
        else:
            if (flag+1 == dictionary_count[i]):
                dict_count[i] += 1
            flag= 0

file[" "]=" "

file["count"] =" "

file.at[0,"count"] = "1"
file.at[1,"count"] = "-1"
file.at[2,"count"] = "2"
file.at[3,"count"] = "-2"
file.at[4,"count"] = "3"
file.at[5,"count"] = "-3"
file.at[6,"count"] = "4"
file.at[7,"count"] = "-4"


file["Longest Subsquence Length"]=" "
file["Count"]=" "

file.at[0, "Longest Subsquence Length"] = dictionary_count[1]
file.at[1, "Longest Subsquence Length"] = dictionary_count[-1]
file.at[2, "Longest Subsquence Length"] = dictionary_count[2]
file.at[3, "Longest Subsquence Length"] = dictionary_count[-2]
file.at[4, "Longest Subsquence Length"] = dictionary_count[3]
file.at[5, "Longest Subsquence Length"] = dictionary_count[-3]
file.at[6, "Longest Subsquence Length"] = dictionary_count[4]
file.at[7, "Longest Subsquence Length"] = dictionary_count[-4]


file.at[0, "Count"] = dict_count[1]
file.at[1, "Count"] = dict_count[-1]
file.at[2, "Count"] = dict_count[2]
file.at[3, "Count"] = dict_count[-2]
file.at[4, "Count"] = dict_count[3]
file.at[5, "Count"] = dict_count[-3]
file.at[6, "Count"] = dict_count[4]
file.at[7, "Count"] = dict_count[-4]

end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
try:
    file.to_excel("output_octant_longest_subsequence.xlsx")
except:
    print("Error Ocurred ")
