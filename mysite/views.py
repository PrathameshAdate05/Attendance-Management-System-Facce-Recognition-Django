import csv
import time
from lib2to3.fixer_util import String

from PIL import ImageGrab
from django.shortcuts import render, HttpResponse, redirect


from mysite.models import studentreg, mon_reports
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,get_user_model,login,logout

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

from datetime import date
import smtplib
from email.message import EmailMessage
import pyttsx3




nameList = []
classNames = []
# Create your views here.
def index(request):
    return render(request,"index.html")


def addStudent(request):
    if request.method=='POST':
        rollno=request.POST['rollno']
        fname=request.POST['fname']
        lname=request.POST['lname']
        enrollmentno=request.POST['enrollmentno']
        phone=request.POST['phone']
        dob=request.POST['dob']
        studentimage=request.POST['studentimage']
        dept=request.POST['dept']
        studentreg(rollno=rollno,fname=fname,lname=lname,enrollmentno=enrollmentno,phone=phone,dob=dob,studentimage=studentimage,dept=dept).save()
        messages.success(request, "Student Registration Completed Successfully..!")
        return render(request,"addStudent.html")
    else:
        return render(request,"addStudent.html")


def facultyEnroll(request):

    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        username = request.POST['uname']
        password=request.POST['password']
        user = User.objects.create_user(username=username,password=password,email=email,first_name=fname,last_name=lname)
        user.save()
        messages.success(request,"Faculty Registration Completed Successfully..!")
        return render(request,"facultyEnroll.html")
    else:
        return render(request,"facultyEnroll.html")

def loginn(request):
    if request.method=="POST":
        username = request.POST['uname']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,"index.html")
        else:
            messages.success(request,"Username or Password is Invalid..!!")
            return render(request,"login.html")

    return render(request,"login.html")

#voice alert method

def tts(msg):
    engine =pyttsx3.init()
    engine.setProperty('rate',180)
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    # say = name+"Your attendance is marked"
    engine.say(msg)
    engine.runAndWait()

# mail sending method
def mail(femail,finame):
    EMAIL = "attendancesystemaitrc@gmail.com"
    PASS = "Aitrc555"
    msg = EmailMessage()
    msg['Subject'] = f"Attendance Report for {finame}"
    msg['From'] = EMAIL
    msg['To'] = femail
    msg.set_content("Thanks for using Our Attendance System")

    # try except block for checking  file is present or not..
    try:
        with open(f'static/Reports/%s'%finame, 'rb') as f:
            file_date = f.read()
            file_name = f.name
    except:
        return "File not found"
    msg.add_attachment(file_date, maintype='application', subtype='octet-stream', filename=file_name)

    # try except block for checking the internet conn is available or not
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASS)
            smtp.send_message(msg)
            smtp.quit()
    except:
        return "Can't Send report Check your connection and try again..!!"
    print('Mail Sent')
    msg = f"Report sent to the {femail}"
    # tts(msg)
    return f"Report sent to the {femail}"

#absent marking method
def absent(finame,period):
    with open('static/Reports/%s'%finame,'a') as f:
        wrt = csv.writer(f)
        for sname in classNames:
            if sname not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                dte = date.today()
                cmonth = datetime.now()
                studetails = studentreg.objects.get(rollno__exact=sname)
                stname = studetails.fname + " " + studetails.lname
                wrt.writerow([sname, stname, dtString, dte, studetails.dept, "Absent"])
                mon_reports(sroll=sname, name=stname, period=period, present_date=dte, present_time=dtString,
                            curmonth=cmonth.strftime("%B"), status="Absent").save()


#main page function
def attendance(request):


    # finding encodings
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    #marking the attendance
    def markAttendance(name, img, faceLoc, finame,peroid):
        # print(finame)
        with open('static/Reports/%s'%finame, 'a') as f:
            wrt = csv.writer(f)
            # myDataList = f.readlines()
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                dte = date.today()
                cmonth = datetime.now()
                nameList.append(name)
                studetails = studentreg.objects.get(rollno__exact=name)
                sname=studetails.fname+" "+studetails.lname
                # print(studetails.Fname)
                # f.writelines(f'\n{name},{dtString}')
                wrt.writerow([name, sname, dtString, dte,studetails.dept, "Present"])
                msg = sname + "Your attendance is marked"
                tts(msg)
                mon_reports(sroll=name,name=sname,period=peroid,present_date=dte,present_time=dtString,curmonth=cmonth.strftime("%B"),status="Present").save()
                # mssg=name+"Your attendace is marked"
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                # cv2.putText( img,mssg , (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                # messages.success()


            else:

                print("already present")
                studetails = studentreg.objects.get(rollno__exact=name)
                sname = studetails.fname + " " + studetails.lname

                mssg = sname + " You are already present"
                tts(mssg)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, mssg, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



    if request.method=="POST":
        period=request.POST['period']
        femail=request.POST['femail']
        timer=request.POST['timer']
        ipcam=request.POST['ipcam']
        finame = str(period)+"-" + str(date.today()) + ".csv" # creating file name according to the period and time

        base_dir = os.getcwd()
        path = 'static/studentImages/'
        images = []

        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])


        encodeListKnown = findEncodings(images)

        print('Encoding Complete')



        cap=cv2.VideoCapture(int(ipcam))#capturing cam


        t=int(timer)
        while t:
            success, img = cap.read()
            actualt=int(t/2)#setting timer calulation
            mins, secs = divmod(actualt, 60)
            timer = '{:02d} : {:02d}'.format(mins, secs)
            print(timer, end=" ")
            cv2.putText(img, timer, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # img = captureScreen()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    # now = datetime.now()
                    # dtString = now.strftime('%H:%M:%S')
                    # print(name, dtString)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    markAttendance(name,img,faceLoc,finame,period)#calling mark attendance method
                    # n = now+timedelta(seconds=1)

                else:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 0, 0), cv2.FILLED)
                    cv2.putText(img, "Unknown", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    unmsg = "Unknown call to admin"
                    tts(unmsg)

            time.sleep(0.5)
            t -= 1
            cv2.imshow('Webcam', img)
            cv2.waitKey(1)
        print("timer ended")
        # releasing cam and destroying all frames..
        cap.release()
        cv2.destroyAllWindows()
        absent(finame,period)
        nameList.clear()
        classNames.clear()
        mssg=mail(femail,finame)
        messages.success(request,mssg)

    return render(request, "attendance.html")

#report method
def report(request):
    if request.method=='POST':
        period = request.POST['period']
        period_date = request.POST['period_date']
        femail = request.POST['femail']
        finame = str(period)+"-"+str(period_date)+".csv"
        mssg = mail(femail,finame)
        messages.success(request,mssg)
    return render(request,"report.html")



def month_report(request):
    # data = mon_reports.objects.all()
    if request.method=='POST':
        rollno = request.POST['rollno']
        month = request.POST['month']

        data = mon_reports.objects.filter(sroll__exact=rollno).filter(curmonth__exact=month)
        # data = mon_reports.objects.all()

    # messages.success(request,"No Data Found..!!")
        if data.exists():
            return render(request, "month_report.html", {"records": data})
        else:
            messages.success(request, "No Data Found..!!")
        print(data)

    # details=studentreg.objects.get(rollno__exact="CM3101")
    # print(details.fname)
    # print(details.lname)

    return render(request,"month_report.html")
