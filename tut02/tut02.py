# import pandas as pd
# df = pd.read_csv (r'octant_output.csv')
# print("sum of octant is ", df['Octant'].sum());
from itertools import count
# from openpyxl import load_workbook
import numpy as np
import math
from multiprocessing.sharedctypes import Value
import pandas as pd
file = pd.read_excel("input_octant_transition_identify.xlsx")
# finding the average value of U, V AND W
average_u = file['U'].mean()
average_v = file['V'].mean()
average_w = file['W'].mean()
# adding this to csv file

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
octant_list = []
for x in range(len(file)):

    if (file["U'=U - U avg"][x] > 0 and file["V'=V - V avg"][x] > 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list.append(1)
        else:
            octant_list.append(-1)

    elif (file["U'=U - U avg"][x] < 0 and file["V'=V - V avg"][x] > 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list.append(2)
        else:
            octant_list.append(-2)

    elif (file["U'=U - U avg"][x] < 0 and file["V'=V - V avg"][x] < 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list.append(3)
        else:
            octant_list.append(-3)

    else:
        if (file["W'=W - W avg"][x] >= 0):
            octant_list.append(4)
        else:
            octant_list.append(-4)

file["octant"] = octant_list

file.at[2, ' '] = "User Input"


def octant_identification(mod=5000):
    file.at[0, "octant ID"] = "overall count"
    file.at[1, "octant ID"] = "Mod {}".format(mod)
    total_range = math.ceil(len(file)/mod)
    start = 0
    for i in range(total_range):

        if (i == total_range-1):
            file.at[i+2, "octant ID"] = "{}-{}".format(start, len(file)-1)
            file.at[i+2+1, "octant ID"] = "Verified"
            file.at[i+2,
                    '1'] = file["octant"].iloc[start:len(file)].value_counts()[1]
            file.at[i+2+1, '1'] = file['1'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '-1'] = file["octant"].iloc[start:len(file)].value_counts()[-1]
            file.at[i+2+1, '-1'] = file['-1'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '2'] = file["octant"].iloc[start:len(file)].value_counts()[2]
            file.at[i+2+1, '2'] = file['2'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '-2'] = file["octant"].iloc[start:len(file)].value_counts()[-2]
            file.at[i+2+1, '-2'] = file['-2'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '3'] = file["octant"].iloc[start:len(file)].value_counts()[3]
            file.at[i+2+1, '3'] = file['3'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '-3'] = file["octant"].iloc[start:len(file)].value_counts()[-3]
            file.at[i+2+1, '-3'] = file['-3'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '4'] = file["octant"].iloc[start:len(file)].value_counts()[4]
            file.at[i+2+1, '4'] = file['4'].iloc[2:total_range+2].sum()
            file.at[i+2,
                    '-4'] = file["octant"].iloc[start:len(file)].value_counts()[-4]
            file.at[i+2+1, '-4'] = file['-4'].iloc[2:total_range+2].sum()
            continue

        file.at[i+2, "octant ID"] = "{}-{}".format(start, start+mod-1)

        file.at[i+2, '1'] = file["octant"].iloc[start:start+mod].value_counts()[1]
        file.at[i+2, '-1'] = file["octant"].iloc[start:start +
                                                 mod].value_counts()[-1]
        file.at[i+2, '2'] = file["octant"].iloc[start:start+mod].value_counts()[2]
        file.at[i+2, '-2'] = file["octant"].iloc[start:start +
                                                 mod].value_counts()[-2]
        file.at[i+2, '3'] = file["octant"].iloc[start:start+mod].value_counts()[3]
        file.at[i+2, '-3'] = file["octant"].iloc[start:start +
                                                 mod].value_counts()[-3]
        file.at[i+2, '4'] = file["octant"].iloc[start:start+mod].value_counts()[4]
        file.at[i+2, '-4'] = file["octant"].iloc[start:start +
                                                 mod].value_counts()[-4]
        start = start+mod


mod = 5000
octant_identification(mod)

# counting total count of unique numbers
file.at[0, '1'] = file["octant"].value_counts()[1]
file.at[0, '-1'] = file["octant"].value_counts()[-1]
file.at[0, '2'] = file["octant"].value_counts()[2]
file.at[0, '-2'] = file["octant"].value_counts()[-2]
file.at[0, '3'] = file["octant"].value_counts()[3]
file.at[0, '-3'] = file["octant"].value_counts()[-3]
file.at[0, '4'] = file["octant"].value_counts()[4]
file.at[0, '-4'] = file["octant"].value_counts()[-4]


total_range = math.ceil(len(file)/mod)
y = total_range+5
file.at[y, "octant ID"] = "overall transition count"
row_index = [1, -1, 2, -2, 3, -3, 4, -4]
index = ['Count', 1, -1, 2, -2, 3, -3, 4, -4]
file.at[y+1, "1"] = "To"
for i in range(1, len(index)+1):
    file.at[y+1+i, "octant ID"] = index[i-1]

file.at[y+2, "1"] = "1"
file.at[y+2, "-1"] = "-1"
file.at[y+2, "2"] = "2"
file.at[y+2, "-2"] = "-2"
file.at[y+2, "3"] = "3"
file.at[y+2, "-3"] = "-3"
file.at[y+2, "4"] = "4"
file.at[y+2, "-4"] = "-4"

# 1,-1,2,-2,3,-3,4,-4
list_total = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]


for i in range(len(file)-1):
    value1 = file["octant"][i]
    value2 = file["octant"][i+1]
    value1_index = index.index(value1)-1
    # print(value1_index)
    value2_index = row_index.index(value2)
    list_total[value1_index][value2_index] += 1
s = 14
for i in range(8):
    file.at[s, "1"] = list_total[i][0]
    file.at[s, "-1"] = list_total[i][1]
    file.at[s, "2"] = list_total[i][2]
    file.at[s, "-2"] = list_total[i][3]
    file.at[s, "3"] = list_total[i][4]
    file.at[s, "-3"] = list_total[i][5]
    file.at[s, "4"] = list_total[i][6]
    file.at[s, "-4"] = list_total[i][7]
    s += 1
# mid transition count
#row_index = [1, -1, 2, -2, 3, -3, 4, -4]
#index = ['Count', 1, -1, 2, -2, 3, -3, 4, -4]

def modtransition_count(mod=5000):
    range_total = math.ceil(len(file)/mod)
    tvalue = 25
    initial = 0
    while(range_total>0):
          # change the tvalue at lat by adding 13
        file.at[tvalue, "octant ID"] = "Mod Transition Count"
    
          # change this value at last by adding mod
        final = initial + mod
        if(final>len(file)):
            final = len(file)-1
        
        file.at[tvalue+1, "octant ID"] = "{}-{}".format(initial, final)
        if(initial!=0):
            file.at[tvalue+1, "octant ID"] = "{}-{}".format(initial+1, final)

        file.at[tvalue+1, "1"] = "To"
        file.at[tvalue+3, " "] = "From"
    
        for i in range(1,len(index)+1):
            file.at[tvalue+1+i, "octant ID"] = index[i-1]

        file.at[tvalue+2, "1"] = "1"
        file.at[tvalue+2, "-1"] = "-1"
        file.at[tvalue+2, "2"] = "2"
        file.at[tvalue+2, "-2"] = "-2"
        file.at[tvalue+2, "3"] = "3"
        file.at[tvalue+2, "-3"] = "-3"
        file.at[tvalue+2, "-4"] = "-4"
        file.at[tvalue+2, "4"] = "4"

        # put the value in transition matrix
        list_total1=[[0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]]

        for i in range(initial,final+1):
            value1 = file["octant"][i]
            value2 = file["octant"][i+1]
            value1_index = index.index(value1)-1
            # print(value1_index)
            value2_index = row_index.index(value2)
            list_total1[value1_index][value2_index] += 1

        s = tvalue+3
        for i in range(8):
            file.at[s, "1"] = list_total1[i][0]
            file.at[s, "-1"] = list_total1[i][1]
            file.at[s, "2"] = list_total1[i][2]
            file.at[s, "-2"] = list_total1[i][3]
            file.at[s, "3"] = list_total1[i][4]
            file.at[s, "-3"] = list_total1[i][5]
            file.at[s, "4"] = list_total1[i][6]
            file.at[s, "-4"] = list_total1[i][7]
            s += 1
        initial = final
        tvalue = tvalue+13
        range_total = range_total-1
    

modtransition_count(mod)


file.to_excel("octant_output.xlsx")
