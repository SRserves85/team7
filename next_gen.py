import shutil
import socket
import time

import face_recognition
import requests
from PIL import Image


ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']  # noqa

# top = Tk()   # Create a top window
# top.title('Sunfounder Raspberry Pi Smart Video Car')

HOST = '192.168.1.217'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server


def forward_fun(event):
    print 'forward'
    tcpCliSock.send('forward')


def backward_fun(event):
    print 'backward'
    tcpCliSock.send('backward')


def left_fun(event):
    print 'left'
    tcpCliSock.send('left')


def right_fun(event):
    print 'right'
    tcpCliSock.send('right')


def stop_fun(event):
    print 'stop'
    tcpCliSock.send('stop')


def home_fun(event):
    print 'home'
    tcpCliSock.send('home')


def x_increase(event):
    print 'x+'
    tcpCliSock.send('x+')


def x_decrease(event):
    print 'x-'
    tcpCliSock.send('x-')


def y_increase(event):
    print 'y+'
    tcpCliSock.send('y+')


def y_decrease(event):
    print 'y-'
    tcpCliSock.send('y-')


def xy_home(event):
    print 'xy_home'
    tcpCliSock.send('xy_home')


def face_detect():
    unknown_image = face_recognition.load_image_file('temp.jpg')
    known_image = face_recognition.load_image_file('known.jpg')
    try:
        scott_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    except:
        print 'No Faces'
        return 'blue'

    for x in face_recognition.compare_faces([scott_encoding], unknown_encoding):
        if x:
            return 'green'

    return 'red'


def grab_image():
    snap = requests.get('http://192.168.1.217:8080/?action=snapshot', stream=True)
    with open('temp.jpg', 'wb') as f:
        snap.raw.decode_content = True
        shutil.copyfileobj(snap.raw, f)

    image = Image.open('temp.jpg')
    image = image.rotate(180)
    image.save('temp.jpg')


if __name__ == '__main__':
    requests.get('http://192.168.1.217:8000/led/setup')
    xy_home()
    while True:
        grab_image()
        match = face_detect()
        if match == 'green':
            requests.get('http://192.168.1.217:8000/led/set_green')
            break

        elif match == 'red':
            requests.get('http://192.168.1.217:8000/led/set_red')

        elif match == 'blue':
            requests.get('http://192.168.1.217:8000/led/set_blue')

        else:
            print 'invalid state'

        forward_fun()
        time.sleep(1)
        stop_fun()

    stop_fun()
    requests.get('http://192.168.1.217:8000/led/destroy')
