import shutil
import time
from socket import * 

import face_recognition
import requests
from PIL import Image

ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

top = Tk()   # Create a top window
top.title('Sunfounder Raspberry Pi Smart Video Car')

HOST = '192.168.1.217'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server



def face_detect():
    unknown_image = face_recognition.load_image_file('temp.jpg')
    known_image = face_recognition.load_image_file('known.jpg')

    try:
        scott_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    except:
        print "NO FACES!!"
        return False

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
            print "NOT MATCHED"
            # requests.get('http://192.168.1.217:8000/led/red')
            pass
        time.sleep(1)
