from datetime import datetime
from multiprocessing.sharedctypes import Value
start_time = datetime.now()
import pandas as pd
import math
file = pd.read_excel("octant_input.xlsx")
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

file["Rank 1"] =""
file["Rank 2"] = ""
file["Rank 3"] = ""
file["Rank 4"] = ""
file["Rank 5"] = ""
file["Rank 6"] = ""
file["Rank 7"] = ""
file["Rank 8"] = ""
file["Rank1 Octant ID"]=""
file["Rank1 Octant Name"] = ""

no_list = ['1', '-1', '2', '-2', '3', '-3', '4', '-4']
count_list =[]

for i in range(8):
    count_list.append(file.at[0, no_list[i]])

print(count_list)
dict_count = {count_list[0]: 0, count_list[1]: 0, count_list[2]: 0, count_list[3]: 0, count_list[4]: 0, count_list[5]: 0, count_list[6]: 0, count_list[7]: 0}
start_1 =8

# print(max(count_list))
#assigning values from 1 to 8
for i in range(8):
    mini = min(count_list)
    dict_count[mini] = start_1
    count_list.remove(mini)
    start_1-=1
print(dict_count)
# print the values in xlsx in file
start_cout =1
for values in dict_count.values():
    # print(values)
    file.at[0, "Rank {}".format(start_cout)] = values
    start_cout+=1
for i in range(8):
    if(file.at[0, "Rank {}".format(i+1)] ==1):
            if(i==0):
                file.at[0, "Rank1 Octant ID"] = 1
                file.at[0, "Rank1 Octant Name"] = "Internal outward interaction"
            if(i==1):
                file.at[0, "Rank1 Octant ID"] = -1
                file.at[0, "Rank1 Octant Name"] = "External outward interaction"
            if(i==2):
                file.at[0, "Rank1 Octant ID"] = 2
                file.at[0, "Rank1 Octant Name"] = "External Ejection"
            if(i==3):
                file.at[0, "Rank1 Octant ID"] = -2
                file.at[0, "Rank1 Octant Name"] = "Internal Ejection"
            if(i==4):
                file.at[0, "Rank1 Octant ID"] = 3
                file.at[0, "Rank1 Octant Name"] = "External inward interaction"
            if(i==5):
                file.at[0, "Rank1 Octant ID"] = -3
                file.at[0, "Rank1 Octant Name"] = "Internal inward interaction"
            if(i==6):
                file.at[0, "Rank1 Octant ID"] = 4
                file.at[0, "Rank1 Octant Name"] = "Internal sweep"
            if(i==7):
                file.at[0, "Rank1 Octant ID"] = -4
                file.at[0, "Rank1 Octant Name"] = "External sweep"

# for mod

def priority_order(mod =5000):
    total_range = math.ceil(len(file)/mod)
    count_list1 =[]
    start_cout_1 =0
    for i in range(total_range):
        for i in range(8):
            count_list1.append(file.at[start_cout_1+2, no_list[i]])
       
        dict_count_1 = {count_list1[0]: 0, count_list1[1]: 0, count_list1[2]: 0, count_list1[3]: 0, count_list1[4]: 0, count_list1[5]: 0, count_list1[6]: 0, count_list1[7]: 0}

        start1 =8
        for i in range(8):
            mini1 = min(count_list1)
            dict_count_1[mini1] = start1
            count_list1.remove(mini1)
            start1-=1

        start_cout =1
        for values in dict_count_1.values():      
            file.at[start_cout_1+2, "Rank {}".format(start_cout)] = values
            start_cout+=1

        ## rank1 octant ID
        for i in range(8):
            if(file.at[start_cout_1+2, "Rank {}".format(i+1)] ==1):
                if(i==0):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = 1
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "Internal outward interaction"
                if(i==1):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = -1
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "External outward interaction"
                if(i==2):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = 2
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "External Ejection"
                if(i==3):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = -2
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "Internal Ejection"
                if(i==4):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = 3
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "External inward interaction"
                if(i==5):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = -3
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "Internal inward interaction"
                if(i==6):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = 4
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "Internal sweep"
                if(i==7):
                    file.at[start_cout_1+2, "Rank1 Octant ID"] = -4
                    file.at[start_cout_1+2, "Rank1 Octant Name"] = "External sweep"
        start_cout_1 +=1


 
priority_order(mod)
total_range = math.ceil(len(file)/mod)
numb_list =["Octant ID", 1,  -1, 2, -2, 3, -3, 4, -4]
octant_name_list =["Octant Name","Internal outward interaction", "External outward interaction", "External Ejection", "internal Ejection", "External inward interaction", "Internal inward interaction", "Internal sweep", "External sweep"]
count_of_no = []
for i in range(total_range):
    count_of_no.append(file.at[2+i,"Rank1 Octant ID"])
for i in range(8):
    file.at[5+total_range+i+1, "1"] = numb_list[i]
    file.at[5+total_range+i+1, "-1"] = octant_name_list[i]
      
file.at[5+total_range, "2"] = "Count of Rank 1 Mod Values"

file.at[5+total_range+1, "2"] = count_of_no.count(1)
file.at[5+total_range+2, "2"] = count_of_no.count(-1)
file.at[5+total_range+3, "2"] = count_of_no.count(2)
file.at[5+total_range+4, "2"] = count_of_no.count(-2)
file.at[5+total_range+5, "2"] = count_of_no.count(3)
file.at[5+total_range+6, "2"] = count_of_no.count(-3)
file.at[5+total_range+7, "2"] = count_of_no.count(4)
file.at[5+total_range+8, "2"] = count_of_no.count(-4)


#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
file.to_excel("octant_output_temp.xlsx")






