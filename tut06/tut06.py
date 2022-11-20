import pandas as pd
from datetime import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


from random import randint
from time import sleep


start_time = datetime.now()


date = datetime(2022, 7, 26)
day_next = timedelta(1)


file = pd.read_csv("input_attendance.csv")
students_in_CS384 = pd.read_csv("input_registered_students.csv")

student_list = {}


k = 0
for i in students_in_CS384.loc[:, "Roll No"]:
    student_list[i] = students_in_CS384.loc[k,"Name"]
    k += 1


attend_valid_days = [] # here we get the number of days when a student attended the lecture

attendance_lastdays = datetime( 
    int(file.iloc[-1,0][6:10]), 
    int(file.iloc[-1,0][3:5]), 
    int(file.iloc[-1,0][:2]))
i = 1

while date < attendance_lastdays:
    if(date.weekday() == 0):
        attend_valid_days.append(str(datetime.strftime(date,  "%d-%m-%Y")))
        date += day_next
        date += day_next
        date += day_next
    elif(date.weekday() == 3):
        attend_valid_days.append(str(datetime.strftime(date,  "%d-%m-%Y")))
        date += day_next
        date += day_next
        date += day_next
        date += day_next
    else:
        date += day_next

data = {}

for i in attend_valid_days:
    student_data = {}

    for j in student_list.keys():
        student_data[j] = {"total_attendance" : 0,
        "real_attendance" : 0, 
        "duplicate_attendance": 0, 
        "invalid_attendance" : 0, 
        "total_absent" : 1}
    data[i] = student_data

total_attendance_CS384 = {}
for i in student_list.keys():
    total_attendance_CS384[i] = {"total_attendance" : 0,
    "real_attendance" : 0, 
    "duplicate_attendance": 0, 
    "invalid_attendance" : 0, 
    "total_absent" : 1}

flag = 0
k = 0
for i in file.loc[:, "Attendance"]:
    i = str(i)[:8]                  
    j = file.iloc[k, 0]              
    student_date_attendedlecture = j[:10]
    
  
    if(i.upper() in student_list.keys() and student_date_attendedlecture in attend_valid_days):
        data[student_date_attendedlecture][i.upper()]["total_attendance"] += 1
        if("14:00" <= j[-5:] <= "15:00" and data[student_date_attendedlecture][i.upper()]["total_attendance"] - data[student_date_attendedlecture][i.upper()]["invalid_attendance"] > 1):
            data[student_date_attendedlecture][i.upper()]["duplicate_attendance"] += 1
            data[student_date_attendedlecture][i.upper()]["total_absent"] = 0
        elif("14:00" <= j[-5:] <= "15:00"):
            data[student_date_attendedlecture][i.upper()]["real_attendance"] = 1
            data[student_date_attendedlecture][i.upper()]["total_absent"] = 0
        else:
            data[student_date_attendedlecture][i.upper()]["invalid_attendance"] += 1
    k = k + 1


for i,j in student_list.items():
    column = ["Date", "Roll", "Name", "Total Attendance Count", "Real", "Duplicate","Invalid", "Absent"]
    file_individual = pd.DataFrame(columns=column)
    file_individual.at[0, "Roll"] = i.upper()
    file_individual.at[0, "Name"] = j.upper()
    
    k = 1
    for l in attend_valid_days:
        file_individual.at[k, "Date"] = l
        file_individual.at[k,"Total Attendance Count"] = data[l][i]["total_attendance"]
        file_individual.at[k, "Real"] = data[l][i]["real_attendance"]
        file_individual.at[k, "Duplicate"] = data[l][i]["duplicate_attendance"]
        file_individual.at[k, "Invalid"] = data[l][i]["invalid_attendance"]
        file_individual.at[k, "Absent"] = data[l][i]["total_absent"]
        k += 1

    file_individual.to_excel("output/{}.xlsx".format(i), index = False)



column = ["Roll", "Name"]
file_all_data = pd.DataFrame(columns = column)
k = 1
for i,j in student_list.items():
    file_all_data.at[k, "Roll"] = i
    file_all_data.at[k, "Name"] = j
    k += 1


stud_attendance = dict()
for i in student_list:
    stud_attendance[i] = 0

for i in attend_valid_days:
    file_all_data[i] = ""
    k = 1
    for j in student_list.keys():
        if(data[i][j.upper()]["real_attendance"]):
            file_all_data.at[k, i] = "P"
            stud_attendance[j] += 1
        else:
            file_all_data.at[k, i] = "A"

        k += 1
        

total_lecture = len(attend_valid_days)

file_all_data["Actual Lecture Taken"] = total_lecture
file_all_data["Total Real"] = ""
file_all_data["% Attendance"] = ""

k = 1
for i in student_list.keys():
    file_all_data.at[k, "Total Real"] = stud_attendance[i]
    file_all_data.at[k, "% Attendance"] = round(stud_attendance[i]/total_lecture*100, 2)
    k += 1


file_all_data.to_excel("output/attendance_report_consolidated.xlsx", index = False)


###########EMAIL BODY################

def send_mail(fromaddr, frompasswd, toaddr, msg_subject, msg_body, file_path):
    try:
        msg = MIMEMultipart()
        print("[+] Message Object Created")
    except:
        print("[-] Error in Creating Message Object")
        return

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = msg_subject

    body = msg_body

    msg.attach(MIMEText(body, 'plain'))

    filename = file_path
    attachment = open(filename, "rb")

    p = MIMEBase('application', 'octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    try:
        msg.attach(p)
        print("[+] File Attached")
    except:
        print("[-] Error in Attaching file")
        return

    try:
        s = smtplib.SMTP('stud.iitp.ac.in', 587)
        print("[+] SMTP Session Created")
    except:
        print("[-] Error in creating SMTP session")
        return

    s.starttls()

    try:
        s.login(fromaddr, frompasswd)
        print("[+] Login Successful")
    except:
        print("[-] Login Failed")

    text = msg.as_string()

    try:
        s.sendmail(fromaddr, toaddr, text)
        print("[+] Mail Sent successfully")
    except:
        print('[-] Mail not sent')

    s.quit()


def isEmail(x):
    if ('@' in x) and ('.' in x):
        return True
    else:
        return False


FROM_ADDR = "rajat_2001ce48@iitp.ac.in"
FROM_PASSWD = "putpasswordhere"      # put your email na password


Subject = "Attendance Report of 2024 batch"
Body ='''
Dear Sir

Please find the attached attendance report of CS384 course.

Thank you
Rajat Jakhar
2001CE48
'''


file_path = "output/attendance_report_consolidated.xlsx"

TO_ADDR = "cs384@iitp.ac.in"

send_mail(FROM_ADDR, FROM_PASSWD, TO_ADDR, Subject, Body, file_path)


#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
