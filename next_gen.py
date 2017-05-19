import shutil
import time

import face_recognition
import requests
from PIL import Image


def face_detect():
    unknown_image = face_recognition.load_image_file('temp.jpg')
    known_image = face_recognition.load_image_file('known.jpg')

    try:
        scott_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    except:
        print ':('

    for x in face_recognition.compare_faces([scott_encoding], unknown_encoding):
        if x:
            return True
            print "BOOM BABY!!"


def grab_image():
    snap = requests.get('http://192.168.1.217:8080/?action=snapshot', stream=True)
    with open('temp.jpg', 'wb') as f:
        snap.raw.decode_content = True
        shutil.copyfileobj(snap.raw, f)

    image = Image.open('temp.jpg')
    image = image.rotate(180)
    image.save('temp.jpg')

if __name__ == '__main__':
    # requests.get('http://192.168.1.217:8000/led/red')
    while True:
        grab_image()
        match = face_detect()
        if match:
            print 'MATCHED'
            # requests.get('http://192.168.1.217:8000/led/green')
            pass
        else:
            # requests.get('http://192.168.1.217:8000/led/red')
            pass
        time.sleep(1)
