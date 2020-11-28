#!/usr/bin/env python
# -*- coding: utf-8 -*-

# decodifica códigos de barra y proporciona la info del código, EAN13...
# y retorna además la lectura entrecomillada

import time
import sys
import cv2
import zbar
from PIL import Image

reload(sys)
sys.setdefaultencoding('utf-8')

# camara USB
camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)

#width=320
#height=240

time.sleep(0.1)
print "Camera lista!"

cv2.namedWindow("Barcode Scanner", 320)

print "OpenCV versión: %s" % (cv2.__version__)
print "Pulse Q para salir ..."

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

# Capture frames from the camera
#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True:
    # Captura frame-by-frame
    output, frame = camera.read()

    # as raw NumPy array
    #output = frame.array.copy()

    # raw detection code
    #gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY, dstCn=0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    pil = Image.fromarray(gray)
    width, height = pil.size
    #raw = pil.tostring()
    raw = pil. tobytes()
    
    # create a reader
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)

    # extract results
    for symbol in image:
        # do something useful with results
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data.decode('utf-8')

    # show the frame
    cv2.imshow("Barcode Scanner", frame)

    # clear stream for next frame
    #rawCapture.truncate(0)
    
    # Wait for the magic key
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord('q'):
    	break

# When everything is done, release the capture
camera.release()
cv2.destroyAllWindows()
