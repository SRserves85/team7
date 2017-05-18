import face_recognition
from PIL import Image

unknown_image = face_recognition.load_image_file('temp.jpg')
known_image = face_recognition.load_image_file('known.jpg')

try:
    scott_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
except:
    print ':('

for x in face_recognition.compare_faces([scott_encoding], unknown_encoding):
    if x == True:
        print "BOOM BABY!!"

