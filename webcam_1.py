#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# prueba camara reconocimiento facial

import cv2
import sys

#cascPath = sys.argv[1]
cascPath = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
cascPath = "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# grosor del trazo que delimita el rostro
thickness = 1

video_capture = cv2.VideoCapture(0)
# dimensiones del frame
# video_capture.set(3,640)
# video_capture.set(4,480)
# reducir el marco de la captura para procesar mas rapido
video_capture.set(3,320)
video_capture.set(4,240)
print "Camera lista!"

print "OpenCV versión: %s" % (cv2.__version__)
print "Pulse Q para salir ..."

while True:
    # Captura frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# variando el factor de escala se produce mayor fluidez
	# pero menor precisión con 1.1 va lento pero calcula muy bien
    # con 1.6 no va fluido pero es aceptable, por encima de 1.8
    # va muy fluido pero tiene menos tiempo para calcular
    
    # el tamaño minimo original de prueba era de 30, 30 
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.9,
        minNeighbors=5,
        minSize=(10, 10),
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        # cv versión 4 y posterior
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # dibujar el rectángulo facial, para que la cara salga completa, no
    # solo el contorno interno, y se amplía hacia arriba y el ancho se
    # agranda para tener un plano más completo del rostro, se pueden
    # parametrizar los valores 15 para el origen x,y y 10 y 25 para ancho y alto
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y-15), (x+w, y+h+10), (0, 255, 0), thickness)
        cv2.rectangle(frame, (x-42, y-36), (x+w+25, y+h+41), (0, 255, 0), thickness)
        # guardar los rostros detectados, aunque se repitan, luego sirve como
        # patrones de aprendizaje, salva solo el rectángulo del rostro, además
        # no ocupan demasiado, aprox. 8 kb
        sub_face = frame[y-35:y+h+30, x-40:x+w+20]
        FaceFileName = "unknowfaces/face_" + str(y) + ".jpg"
        # print FaceFileName
        cv2.imwrite(FaceFileName, sub_face)

    # sobreponer al frame actual
    cv2.imshow('Captura', frame)

    # tecla q para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# liberar el vídeo y destruir la ventana de visualización
video_capture.release()
cv2.destroyAllWindows()

