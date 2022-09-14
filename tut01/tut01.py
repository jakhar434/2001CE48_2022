# def octact_identification(mod=5000):
# ###Code


# from platform import python_version
# ver = python_version()

# if ver == "3.8.10":
#     print("Correct Version Installed")
# else:
#     print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

# mod=5000
# octact_identification(mod)
# import pandas as pd
# df = pd.read_csv (r'octant_output.csv')
# print("sum of octant is ", df['Octant'].sum());
import csv

with open('octant_input.csv', 'r') as file:
    sum_u =0
    sum_v=0
    sum_w =0
    length =0
    read = csv.reader(file)
    for row in read:
        length+=1
        if(length == 1):
            continue
        sum_u = sum_u+float(row[1])
        sum_v = sum_v +float(row[2])
        sum_w = sum_w +float(row[3])
    print(sum_u/length)
    print(sum_v/length)
    print(sum_w/length)

        
