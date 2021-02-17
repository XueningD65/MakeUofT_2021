#
#  major_page.py
#  MakeUofT_2021
#
#  Created by Xuening & Mengzhu on 2021-02-16.
#  Copyright © 2021 Xuening & Mengzhu. All rights reserved.
#

import tkinter as tk
from tkinter import *
from tkinter import ttk
import calendar
from tkinter import colorchooser as cc
import oscilloscope as oscill

from tkinter import *
from PIL import ImageTk,Image

import serial
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

global bgc
bgc = "black"
global canvas
global img_gif_1

def create(name,login):
    #main_page = tk.Tk()
    date = calendar.datetime.datetime

    def enter_potentiometer():
        print("Studying potentiometer...")
        app = oscill.oscilloscope()
        oscill.start_ani()
        app.mainloop()

    def pick_colour():
        colour_name = cc.askcolor(parent = main_page)
        colour_name = colour_name[1]

        global bgc
        bgc = colour_name
        name_label['fg'] = bgc

    def display_image():
        global canvas
        canvas.create_image(200, 200, image=img_gif_1)
        #print("hiiii")
        #img_label = tk.Label(main_page, text="Welcome to the Electrical Circuit Tutorials! Dear " + name)
        #img_label.grid(row=4, column=1)

    login.destroy()
    main_page = tk.Tk()
    main_page.title("Tutorial List")
    main_page.geometry('800x640')

    colour_but = tk.Button(main_page, text="Change colour", command=pick_colour)
    colour_but.grid(row=2, column=0)

    pot_but = tk.Button(main_page, text="Potentiometer", command=enter_potentiometer)
    pot_but.grid(row=3, column=0)

    img_but = tk.Button(main_page, text="image", command=display_image)
    img_but.grid(row=4, column=0)
###
    name_label = tk.Label(main_page, text = "Welcome to the Electrical Circuit Tutorials! Dear "+name)
    today = date.today()
    date_info = today.strftime("%d/%b/%Y %H:%M:%S")
    date_label = tk.Label(main_page, text="Today is "+date_info)
    name_label.grid(row=0, column=1)
    date_label.grid(row=1, column=1)
    global canvas
    global img_gif_1
    canvas = Canvas(main_page, width=600, height=500)
    canvas.grid(row=4, column=1)


    img_gif_1 = ImageTk.PhotoImage(Image.open("D:/Peach__Happer/ECE大三/hackathon/1.png"))

    main_page.mainloop()

root = tk.Tk()
create("Mengzhu", root)