import os, time
import re
import cv2


def controlDirectory():
    path = "CopperPictures"
    control = os.path.exists(path)
    print("Directory found" if control == True else "Directory not found")
    if control == True:
        takeName()


def takeName():
    liste = []
    name = input("File Name ? ")
    number = input("Number ? ")
    if int(len(re.findall("%d+", f"{name}"))) == 0 and int(len(re.findall("%D+", f"{number}"))) == 0:
        liste.append(name)
        liste.append(number)
        callCam(liste)
    else:
        print("variables entered incorrectly")


def callCam(liste):
    global webCam, facecascade
    webCam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    a = 0
    facecascade = cv2.CascadeClassifier("face.xml")

    def openCam(a):
        while a < int(liste[1]):
            time.sleep(0.05)
            img = readCam()
            for (x, y, w, h) in detectFace(img):
                a += 1
                name = str(a) + liste[0]
                dressFace(img, x, y, w, h)
                recordFile(name, img, x, y, w, h)
            cv2.imshow('Webcam', img)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        webCam.release()
        cv2.destroyAllWindows()

    def readCam():
        return webCam.read()[1]

    def detectFace(img):
        return facecascade.detectMultiScale(img, 1.2, 4)

    def dressFace(img, x, y, w, h):
        return cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 1)

    def recordFile(name, img, x, y, w, h):
        return cv2.imwrite("CopperPictures/{}.jpg".format(name), img[y:y + h, x: x + w])

    openCam(a)


controlDirectory()
