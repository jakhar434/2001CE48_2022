# import pandas as pd
# df = pd.read_csv (r'octant_output.csv')
# print("sum of octant is ", df['Octant'].sum());
import csv
import pandas as pd
file = pd.read_csv("octant_input.csv")
#finding the average value of U, V AND W
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
octant_list =[]
for x in range(len(file)):
    
    if (file["U'=U - U avg"][x] > 0 and file["V'=V - V avg"][x] > 0):
        if (file["W'=W - W avg"][x] >= 0):
            octant_list.append(1)
        else:
            octant_list.append(-1)

    elif (file["U'=U - U avg"][x] < 0 and file["V'=V - V avg"][x]> 0):
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

file["octant"]= octant_list
file.at[2, ' ']="User Input"
file.at[0, 'Octant ID'] =' '
file.at[0, '1'] = file["octant"].value_counts()[1]
file.at[0, '-1'] = file["octant"].value_counts()[-1]
file.at[0, '2'] = file["octant"].value_counts()[2]
file.at[0, '-2'] = file["octant"].value_counts()[-2]
file.at[0, '3'] = file["octant"].value_counts()[3]
file.at[0, '-3'] = file["octant"].value_counts()[-3]
file.at[0, '4'] = file["octant"].value_counts()[4]
file.at[0, '-4'] = file["octant"].value_counts()[-4]

file.to_csv("octant_1.csv")
