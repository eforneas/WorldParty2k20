#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Interfaz para procesar Imagenes

import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import time
import cv2
import numpy as np
from subprocess import check_output
from pyscreenshot import grab
from threading import Thread, Lock

once = True
img_screenshot = None

class App:
    original_image = None
    hsv_image = None
    # switch to make sure screenshot not taken while already pressed
    taking_screenshot = False

    def __init__(self, master):
        self.img_path = None
        frame = tk.Frame(master)
        frame.grid()
        root.title("Retoque de imágenes")

        width  = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.geometry('{}x{}'.format(width,height))

        #self.hue_lbl = tk.Label(text="Hue", fg='red')
        #self.hue_lbl.grid(row=2)

        self.low_hue = tk.Scale(master, label='Low',from_=0, to=179, length=200,showvalue=2,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_hue.place(x=0, y=50)

        self.high_hue = tk.Scale(master,label='High', from_=0, to=179, length=200,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_hue.place(x=200, y=50)
        self.high_hue.set(179)
###########################################################################################################
        #self.sat_lbl = tk.Label(text="Saturation", fg='green')
        #self.sat_lbl.grid(row=5)

        self.low_sat = tk.Scale(master, label='Low',from_=0, to=255, length=200,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_sat.place(x=0,y=120)

        self.high_sat = tk.Scale(master, label="High", from_=0, to=255, length=200,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_sat.place(x=200,y=120)
        self.high_sat.set(255)
###########################################################################################################
        #self.val_lbl = tk.Label(text="Value", fg='Blue')
        #self.val_lbl.grid(row=8)

        self.low_val = tk.Scale(master, label="Low",from_=0, to=255, length=200,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_val.place(x=0,y=190)

        self.high_val = tk.Scale(master, label="High",from_=0, to=255, length=200,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_val.place(x=200,y=190)
        self.high_val.set(255)
        #self.high_val.grid(row=10)

###########################################################################################################
# buttons
        #self.print_btn = tk.Button(text='Print', command=self.print_values)
        #self.print_btn.place(x=0,y=250)

        # Open
        self.open_btn = tk.Button(text="Open", command=self.open_file)
        self.open_btn.place(x=0,y=10)
        #self.open_btn.grid(row=6, column=1)

###########################################################################################################
        # timer label
        #self.screenshot_timer_lbl = tk.Label(text="Timer", fg='Red')
        #self.screenshot_timer_lbl.grid(row=8, column=1)

########################################################################################################## Images
        # images
        self.hsv_img_lbl = tk.Label(text="HSV", image=None)
        self.hsv_img_lbl.place(x=790,y=380)
        #self.hsv_img_lbl.grid(row=0, column=0)

        self.original_img_lbl = tk.Label(text='Original',image=None)
        self.original_img_lbl.place(x=790,y=0)
        #self.original_img_lbl.grid(row=0, column=1)
##########################################################################################################
    def open_file(self):
        global once
        once = True
        img_file = tkFileDialog.askopenfilename()   # Buscar Archivo
        # this makes sure you select a file
        # otherwise program crashes if not
        if img_file  != '':      # Si La imagen existe
            self.img_path = img_file
            # Esto solo se asegura de que la imagen se muestra despues de abrirlo
            self.low_hue.set(self.low_hue.get()+1)
            self.low_hue.set(self.low_hue.get()-1)
        else:
            print('No se Selecciono Nada')
            return 0

    def show_changes(self, *args):
        global once, img_screenshot

        if self.img_path == None:  # Si la imagen no hace nada
            return 0

        # obtener valores de los sliders
        # Bajos
        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        # Altos
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()
        # No hace nada si los valores bajos van mas altos que los valores altos
        if low_val > high_val or low_sat > high_sat or low_hue > high_hue:
            return 0

        # Establece la imagen original una vez, manipula la copia en las siguientes iteraciones
        if once:
            # Obtiene la imagen del archivo
            if self.img_path != 'screenshot':
                #img_path = 'objects.png'
                # carga BGR
                self.original_image = cv2.imread(self.img_path,1)
                # image resized
                self.original_image = self.resize_image(self.original_image)
                self.hsv_image = self.original_image.copy()
                #convierte imagen a HSV
                self.hsv_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_BGR2HSV)

            # gets screenshot
            else:
                self.original_image = img_screenshot
                self.hsv_image = img_screenshot.copy()
                #converts image to HSV
                self.hsv_image = cv2.cvtColor(self.hsv_image, cv2.COLOR_BGR2HSV)

            # OpenCV representa imagenes en orden BGR;
            #Sin embargo PIL representa imagenes en orden RGB, por lo que tenemos que intercambiar los canales
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

            # convierte imagen a formato PIL
            self.original_image = Image.fromarray(self.original_image)#.resize((500,500), Image.ANTIALIAS)
            # convierta a formato ImageTk
            self.original_image = ImageTk.PhotoImage(self.original_image)
            # Actualizar la etiqueta de la imagen original
            self.original_img_lbl.configure(image=self.original_image)
            # Keeping a reference! b/ need to!
            #Mantener una referencia! B / necesidad de!
            self.original_img_lbl.image = self.original_image
            once = False

        # Define los valores inferior y superior de la mascara
        # define range of colors in HSV (hue up to 179, sat-255, value-255
        lower_color = np.array([low_hue,low_sat,low_val])
        upper_color= np.array([high_hue,high_sat,high_val])
        # red - 0,255,255 (low (hue-10,100,100) high(hue+10,255,255)
        # green 60,255,255
        # blue -120,255,255

        #crea una mascara con el resultado
        mask = cv2.inRange(self.hsv_image, lower_color, upper_color)
        #res = cv2.bitwise_and(self.original_image.copy(), self.original_image.copy(), mask=mask)

        # convierte a formato RGB
        #maskbgr = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
        #maskrgb = cv2.cvtColor(maskbgr, cv2.COLOR_BGR2RGB)
        # convierte a formato PIL
        mask = Image.fromarray(mask)
        # convierte a formato ImageTk
        mask = ImageTk.PhotoImage(mask)
        # Ajuste de la imagen de hsv a tk etiqueta de imagen
        self.hsv_img_lbl.configure(image=mask)
        # adding a reference to the image to Prevent python's garbage collection from deleting it
        #Anadiendo una referencia a la imagen para evitar que python garbage collection lo elimine
        self.hsv_img_lbl.image = mask

    def resize_image(self,img,*args):
        # Desembala anchura, altura
        height, width,_ = img.shape
        print("Original size: {} {}".format(width, height))
        count_times_resized = 0
        while width > 500 or height > 500:
        #if width > 300 or height > 300:
            # divides images WxH by half
            width = width / 2
            height = height /2
            count_times_resized += 1
        # prints x times resized to console
        if count_times_resized != 0:
            print("Resized {}x smaller, to: {} {}".format(count_times_resized*2,width, height))
        # makes sures image is not TOO small
        if width < 300 and height < 300:
            width = width * 2
            height = height * 2

        img = cv2.resize(img,(width,height))

        return img

# Instance of Tkinter
root = tk.Tk()
# New tkinter instnace of app
app = App(root)
# loops over to keep window active
root.mainloop()
