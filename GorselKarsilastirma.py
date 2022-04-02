import os, re, string
import time
from datetime import datetime
import cv2
import face_recognition
import numpy as np
import mysql.connector


def images():
    Images = []
    classNames = []
    path = "CopperPictures"
    for cl in os.listdir(path):
        Images.append(cv2.imread(f'{path}/{cl}'))
        classNames.append(os.path.splitext(cl)[0])
    print(len(Images))
    return Images, classNames


Images, Names = images()[0], images()[1]
print(Images, Names)


def findEncode(Images):
    encodeList = []
    for img in Images:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeList = findEncode(Images)


def nameS(name):
    return re.findall("\D+", str(name))[0]


def frame(fLoc, img, name):
    y1, x2, y2, x1 = fLoc
    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)


def timeSettings(now=datetime.today()):
    return now.hour * 3600 + now.minute * 60 + now.second


def camRead(webcam):
    return webcam.read()[1]


def openCam():
    global webcam
    webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    targetList, targetTimeList = list(), list()
    while True:
        timeNow = timeSettings()
        img = camRead(webcam)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            # print(encodeFace, encodeListKnown)
            matches = face_recognition.compare_faces(encodeList, encodeFace)
            faceDis = face_recognition.face_distance(encodeList, encodeFace)
            matchindex = np.argmin(faceDis)
            if matches[matchindex]:
                name = Names[matchindex]
                name = nameS(name)
                if name in targetList:
                    order = targetList.index(name)
                    if targetTimeList[order] + 10 < timeNow:
                        timeEnd = timeSettings()
                        frame(faceLoc, img, name)
                        # mysqlConnect(name)
                    else:
                        frame(faceLoc, img, name)
                else:
                    frame(faceLoc, img, name)
                    targetList.append(name)
                    timeEnd = timeSettings()
                    targetTimeList.append(timeEnd)
                    # mysqlConnect(name)
            else:
                print("Bulamadım!")
        print("Name_list , Time_list", targetList, targetTimeList)
        cv2.imshow('Webcam', img)
        if (cv2.waitKey(20) & 0xFF == ord('q')): break
    webcam.release()
    cv2.destroyAllWindows()


"""
def mysqlConnect(name):
    tableName = "targets"
    database = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="targets"
    )
    pencil = database.cursor()
    run = checkTable(pencil, tableName)
    if run == True:
        pencil.execute(f"CREATE TABLE  {tableName} (NAME VARCHAR(255),TIME VARCHAR(255))")
        database.commit()
    else:
        print("This Table already exist")


def checkTable(pencil, tableName):
    tableList = []
    x = True
    for x in pencil.execute("SHOW TABLES"):
        tableList.append(x)
    if tableName in tableList:
        x = False
    else:
        x = True
    return x
"""

openCam()
