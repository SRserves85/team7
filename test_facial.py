""" tests the facial reckog
"""

import shutil

from PIL import Image

# import pillow
import requests

if __name__ == '__main__':
    snap = requests.get('http://192.168.1.217:8080/?action=snapshot', stream=True)
    with open('temp.jpg', 'wb') as f:
        snap.raw.decode_content = True
        shutil.copyfileobj(snap.raw, f)

    image = Image.open('temp.jpg')
    image = image.rotate(180)
    image.save('temp.jpg')