#-----------------------------------------------------------------------------
# Name:        photo_booth.py
# Purpose:     crear una ventana con imagen de video webcam   
#
# Author:      Eduardo Forneas
#
# Created:     2018/04/30
# RCS-ID:      $Id: photo_booth.py $
# Copyright:   (c) 2018
# Licence:     GPL3
#-----------------------------------------------------------------------------

#!/usr/bin/python
# -*- coding: utf-8 -*-

# imprescindible pasar como argumento -o/--output directorio (para las tomas)

# import the necessary packages
from __future__ import print_function
from photoboothapp import PhotoBoothApp
from imutils.video import VideoStream
import argparse
import time
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
    help="path to output directory to store snapshots")
ap.add_argument("-p", "--picamera", type=int, default=-1,
    help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warmup
print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
#vs = VideoStream(usePiCamera=args["picamera"] > 0, resolution=(320, 240), framerate=30).start()
#time.sleep(2.0)
# start the app
pba = PhotoBoothApp(vs, args["output"])
pba.root.mainloop()