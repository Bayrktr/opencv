import os, cv2, face_recognition


def fileName():
    return input("File Name ?")


def controlDirectory():
    x = fileName()
    path = "FreshPictures/{}".format(x)
    if os.path.exists("FreshPictures/{}".format(x)):
        print("image found")
        cutPicture(x, path)
    else:
        print("image not found")


def cutPicture(x, path):
    pathTwo = "CopperPictures/{}".format(x)

    def load_and_color():
        file = face_recognition.load_image_file(path)
        file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
        imageLoc(file)

    def imageLoc(file):
        fileLoc = face_recognition.face_locations(file)[0]
        x, y, w, h = fileLoc[0], fileLoc[1], fileLoc[2], fileLoc[3]
        copper = file[int(x) - 20:int(h) + 20, int(w) - 15:int(y)]
        recordImage(copper)

    def recordImage(copper):
        return cv2.imwrite(pathTwo, copper)

    load_and_color()


controlDirectory()
