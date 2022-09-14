# import pandas as pd
# df = pd.read_csv (r'octant_output.csv')
# print("sum of octant is ", df['Octant'].sum());
import csv
import math
import pandas as pd
file = pd.read_csv("octant_input.csv")
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
def octant_identification(mod = 5000):
    file.at[0, "octant ID"]="overall count"
    file.at[1, "octant ID"] ="Mod {}".format(mod)
    total_range = math.ceil(len(file)/mod)
    start=0
    for i in range(total_range):

        if(i== total_range-1):
            file.at[i+2, "octant ID"] = "{}-{}".format(start, len(file)-1)
            file.at[i+2, '1'] = file["octant"].iloc[start:len(file)].value_counts()[1]
            file.at[i+2, '-1'] = file["octant"].iloc[start:len(file)].value_counts()[-1]
            file.at[i+2, '2'] = file["octant"].iloc[start:len(file)].value_counts()[2]
            file.at[i+2, '-2'] = file["octant"].iloc[start:len(file)].value_counts()[-2]
            file.at[i+2, '3'] = file["octant"].iloc[start:len(file)].value_counts()[3]
            file.at[i+2, '-3'] = file["octant"].iloc[start:len(file)].value_counts()[-3]
            file.at[i+2, '4'] = file["octant"].iloc[start:len(file)].value_counts()[4]
            file.at[i+2, '-4'] = file["octant"].iloc[start:len(file)].value_counts()[-4]
            continue

        file.at[i+2, "octant ID"] = "{}-{}".format(start, start+mod-1)
         

        file.at[i+2, '1'] = file["octant"].iloc[start:start+mod].value_counts()[1]
        file.at[i+2, '-1'] = file["octant"].iloc[start:start+mod].value_counts()[-1]
        file.at[i+2, '2'] = file["octant"].iloc[start:start+mod].value_counts()[2]
        file.at[i+2, '-2'] = file["octant"].iloc[start:start+mod].value_counts()[-2]
        file.at[i+2, '3'] = file["octant"].iloc[start:start+mod].value_counts()[3]
        file.at[i+2, '-3'] = file["octant"].iloc[start:start+mod].value_counts()[-3]
        file.at[i+2, '4'] = file["octant"].iloc[start:start+mod].value_counts()[4]
        file.at[i+2, '-4'] = file["octant"].iloc[start:start+mod].value_counts()[-4]
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

file.to_csv("octant_1.csv")
