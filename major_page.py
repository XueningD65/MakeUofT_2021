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
import random

from tkinter import *
from PIL import ImageTk,Image

import serial_circuit as se

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
LARGE_FONT = ("Verdana", 15)
style.use("ggplot")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)
a.grid(True)
a.legend()

global resistance
resistance = [220, 560, 1000, 4700, 10000]

global x,y
x = 1
y = 1

global xList, yList
xList = []
yList = []

global connected, ser, data
connected = 0
data = []

global potentiometer
potentiometer = False

global curr_val, data_read
curr_val = 0
data_read = False

global ani_s
global canvas
global img_gif_1

global image_path
image_path ="/Users/dongxuening/Desktop/MakeUofT_2021/1.png"


global ani

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def start_ani():
    print("Invoked in major")
    global ani
    ani = animation.FuncAnimation(f, animate, interval=200)

def connect():
    global connected, ser
    ser = serial.Serial('/dev/cu.usbmodem141101', 9800, timeout=1)
    connected = 1
    print("hi")

def close():
    global connected, ser
    ser.close()
    connected = 0
    print("bye")


def read_once():
    if (connected == 0):
        print("You are not connected to the board")
    global curr_val, data_read
    data_read = True

    b = ser.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip()  # remove \n and \r
    print("My data read: ", string)
    if (isfloat(string)):
        flt = float(string)
    elif (string == "" and len(data) >= 1):
        flt = data[-1]
    else:
        flt = 0
    curr_val = flt

def show():
  if(connected==1):
      print("Connected to board ")
      tk.messagebox.showinfo(title='Connection', message='Connected')
  else:
      print("Not connected to any board")
      tk.messagebox.showinfo(title='Connection', message='Not Connected')

def animate(i):

    global data
    if (connected == 0):
        return

    b = ser.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip()  # remove \n and \r
    print("curr: ", string)
    if (isfloat(string)):
        flt = float(string)
    elif (string == "" and len(data)>=1):
        flt = data[-1]
    else:
        flt = 0
    data.append(flt)

    data_ot = []
    if (potentiometer==True):
        for num in data:
            data_ot.append(5-num)

    a.clear()
    a.plot(range(len(data)), data, marker='.', color='blue' , label='Vpot', linewidth=0.5)
    a.plot(range(len(data_ot)), data_ot, marker='.', color='red', label='Vres',  linewidth=0.5)

    a.set_ylabel("Voltage")
    a.set_xlabel("Time")
    a.grid(True)
    a.legend()
    time.sleep(0.2)

def create(name,login):
    #main_page = tk.Tk()
    login.destroy()
    date = calendar.datetime.datetime
    start_ani()

    class major(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            tk.Tk.iconbitmap(self)
            tk.Tk.wm_title(self, "Tutorial List")
            #tk.Tk.geometry('800x640')

            container = tk.Frame(self)
            container.grid(row=0, column=0, padx=10, pady=5)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.geometry('1024x1000')


            self.frames = {}

            for F in (page1, serial_page, parallel_page, potentiometer_page, PageOne, PageTwo, oscilloscope_page):
                frame = F(container, self)

                self.frames[F] = frame

                frame.grid(row=0, column=0, sticky="nsew")

            self.show_frame(page1)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

    class page1(tk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            def enter_potentiometer():
                print("Studying potentiometer...")
                app = oscill.oscilloscope()
                oscill.start_ani()
                app.mainloop()

            def pick_colour():
                colour_name = cc.askcolor(parent=self)
                colour_name = colour_name[1]

                global bgc
                bgc = colour_name
                name_label['fg'] = bgc
                date_label['fg'] = bgc

            def display_image():
                global canvas
                canvas.create_image(200, 200, image=img_gif_1)
                print("Studying Serial circuit...")
                se.serial.show_frame(self, se.StartPage)


            label = tk.Label(self, text="Tutorial List", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            colour_but = tk.Button(self, text="Change colour", command=pick_colour)
            colour_but.grid(row=2, column=0)

            pot_but = tk.Button(self, text="Potentiometer", command=lambda: controller.show_frame(potentiometer_page))
            pot_but.grid(row=3, column=0)

            img_but = tk.Button(self, text="Serial", command=lambda: controller.show_frame(serial_page))
            img_but.grid(row=4, column=0)

            para_but = tk.Button(self, text="Parallel", command=lambda: controller.show_frame(parallel_page))
            para_but.grid(row=5, column=0)

            button_4 = tk.Button(self, text="Connect", width=10, command=connect)
            button_4.grid(row=3, column=1, padx=10, pady=5)
            button_5 = tk.Button(self, text="Close", width=10, command=close)
            button_5.grid(row=3, column=2, padx=10, pady=5)

            name_label = tk.Label(self, text="Welcome to the Electrical Circuit Tutorials! Dear " + name)
            today = date.today()
            date_info = today.strftime("%d/%b/%Y %H:%M:%S")
            date_label = tk.Label(self, text="Today is " + date_info)
            name_label.grid(row=0, column=1)
            date_label.grid(row=1, column=1)

            # canvas.create_image(200, 200, image=img_gif_1)
            # canvas.grid(row=2, column=1)

    class serial_page(tk.Frame):
        global R1, R2
        def __init__(self, parent, controller):
            def update_status():
                # Get the current message
                current_status = lab2["text"]
                # If the message is "Working...", start over with "Working"
                if (data_read == False):
                    current_status = " "
                    another = " "
                # If not, then just add a "." on the end
                else:
                    current_status = str(curr_val)
                    another = str(5 - curr_val)
                # Update the message
                lab4["text"] = current_status +" V"
                lab2["text"] = another + " V"
                # After 1 second, update the status
                self.after(100, update_status)

            def check():
                if (data_read == False):
                    print("Haven't read from the board!")
                    return
                print("Checking answer...")
                expected = 5*R2/(R1+R2)
                print("Expected: ", expected)
                obtained = curr_val
                if(obtained>=0.95*expected and obtained<=1.05*expected):
                    print("Correct!")
                    tk.messagebox.showinfo(title='Your Answer', message='Correct')
                else:
                    tk.messagebox.showinfo(title='Your Answer', message='Incorrect')

            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Serial Circuit Image", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            button_b = ttk.Button(self, text="Back to Home",
                                  command=lambda: controller.show_frame(page1))
            button_b.grid(row=1, column=1, padx=10, pady=5)

            button3 = ttk.Button(self, text="Oscilloscope",
                                 command=lambda: controller.show_frame(oscilloscope_page))
            button3.grid(row=5, column=0, padx=10, pady=5)

            button_4 = tk.Button(self, text="Connect", width=10, command=connect)
            button_4.grid(row=5, column=1, padx=10, pady=5)
            button_5 = tk.Button(self, text="Close", width=10, command=close)
            button_5.grid(row=5, column=2, padx=10, pady=5)
            button_6 = tk.Button(self, text="Show Connection", width=10, command=show)
            button_6.grid(row=6, column=0, padx=10, pady=5)

            lab1 = tk.Label(self, text="Voltage over R1: ")
            lab1.grid(row=3, column=0, padx=10, pady=5)
            lab2 = tk.Label(self, text=" ")
            lab2.grid(row=3, column=1, padx=10, pady=5)

            lab3 = tk.Label(self, text="Voltage over R2: ")
            lab3.grid(row=4, column=0, padx=10, pady=5)
            lab4 = tk.Label(self, text=" ")
            lab4.grid(row=4, column=1, padx=10, pady=5)

            button_r = ttk.Button(self, text="Read",command=read_once)
            button_r.grid(row=3, column=2, padx=10, pady=5)
            button_c = ttk.Button(self, text="Check", command=check)
            button_c.grid(row=4, column=2, padx=10, pady=5)

            self.after(100, update_status)

            global canvas
            global img_gif_1
            img_gif_1 = ImageTk.PhotoImage(Image.open(image_path))
            canvas = Canvas(self, width=600, height=500)
            canvas.grid(row=2, column=1)
            canvas.create_image(200, 200, image=img_gif_1)

            random.seed(10)
            R = random.sample(range(0, 4), 3)
            R1 = resistance[R[0]]
            R2 = resistance[R[2]]

            lab_r = tk.Label(self, text="R1 = "+str(R1)+" R2 = "+str(R2))
            lab_r.grid(row=2, column=2, padx=10, pady=5)

            print("R1 = ", R1, " R2 = ", R2)

    class parallel_page(tk.Frame):
        global R1, R2

        def __init__(self, parent, controller):
            def check():
                print("Checking answer...")
                expected_r1 = 5 / R1
                expected_r2 = 5 / R2
                print("Expected: ", expected_r1, " and ", expected_r2)
                obtained_r1 = entry_r1.get()
                obtained_r2 = entry_r2.get()
                if(isfloat(obtained_r1) and isfloat(obtained_r2)):
                    obtained_r1 = float(obtained_r1)
                    obtained_r2 = float(obtained_r2)
                    if (obtained_r1 >= 0.95 * expected_r1 and obtained_r1 <= 1.05 * expected_r1 and obtained_r2 >= 0.95 * expected_r2 and obtained_r2 <= 1.05 * expected_r2):
                        print("Correct!")
                        tk.messagebox.showinfo(title='Your Answer', message='Correct')
                    else:
                        tk.messagebox.showinfo(title='Your Answer', message='Incorrect')
                else:
                    tk.messagebox.showinfo(title='Your Answer', message='Incorrect')

            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Parallel Circuit Image", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            button_b = ttk.Button(self, text="Back to Home",
                                  command=lambda: controller.show_frame(page1))
            button_b.grid(row=1, column=1, padx=10, pady=5)

            button3 = ttk.Button(self, text="Oscilloscope",
                                 command=lambda: controller.show_frame(oscilloscope_page))
            button3.grid(row=5, column=0, padx=10, pady=5)

            button_4 = tk.Button(self, text="Connect", width=10, command=connect)
            button_4.grid(row=5, column=1, padx=10, pady=5)
            button_5 = tk.Button(self, text="Close", width=10, command=close)
            button_5.grid(row=5, column=2, padx=10, pady=5)
            button_6 = tk.Button(self, text="Show Connection", width=10, command=show)
            button_6.grid(row=6, column=0, padx=10, pady=5)

            curr_r1 = tk.StringVar()
            lab1 = tk.Label(self, text="Calculated Current through R1: ")
            lab1.grid(row=3, column=0, padx=10, pady=5)
            entry_r1 = tk.Entry(self, textvariable=curr_r1)
            entry_r1.grid(row=3, column=1, padx=10, pady=5)

            curr_r2 = tk.StringVar()
            lab2 = tk.Label(self, text="Calculated Current through R2: ")
            lab2.grid(row=4, column=0, padx=10, pady=5)
            entry_r2 = tk.Entry(self, textvariable=curr_r2)
            entry_r2.grid(row=4, column=1, padx=10, pady=5)

            button_c = ttk.Button(self, text="Check", command=check)
            button_c.grid(row=4, column=2, padx=10, pady=5)

            global canvas
            global img_gif_3
            img_gif_3 = ImageTk.PhotoImage(Image.open("/Users/dongxuening/Desktop/MakeUofT_2021/2.png"))
            canvas = Canvas(self, width=600, height=500)
            canvas.grid(row=2, column=1)
            canvas.create_image(200, 200, image=img_gif_3)

            random.seed(10)
            R = random.sample(range(0, 4), 3)
            R1 = resistance[R[0]]
            R2 = resistance[R[2]]

            lab_r = tk.Label(self, text="R1 = "+str(R1)+" R2 = "+str(R2))
            lab_r.grid(row=2, column=2, padx=10, pady=5)

            print("R1 = ", R1, " R2 = ", R2)


    class potentiometer_page(tk.Frame):
        global potentiometer
        potentiometer = True
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            label = tk.Label(self, text="Circuit Analysis", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            button_b = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(page1))
            button_b.grid(row=1, column=1, padx=10, pady=5)

            button2 = ttk.Button(self, text="Page Two",
                                 command=lambda: controller.show_frame(PageTwo))
            button2.grid(row=2, column=0, padx=10, pady=5)

            button3 = ttk.Button(self, text="Oscilloscope",
                                 command=lambda: controller.show_frame(oscilloscope_page))
            button3.grid(row=4, column=0, padx=10, pady=5)

            button_4 = tk.Button(self, text="Connect", width=10, command=connect)
            button_4.grid(row=4, column=1, padx=10, pady=5)
            button_5 = tk.Button(self, text="Close", width=10, command=close)
            button_5.grid(row=4, column=2, padx=10, pady=5)
            button_6 = tk.Button(self, text="Show Connection", width=10, command=show)
            button_6.grid(row=5, column=0, padx=10, pady=5)

            lab1 = tk.Label(self, text="Please use the oscilloscope to find V against time")
            lab1.grid(row=3, column=1, padx=10, pady=5)

            global canvas
            global img_gif_2
            img_gif_2 = ImageTk.PhotoImage(Image.open("/Users/dongxuening/Desktop/MakeUofT_2021/3.png"))
            canvas = Canvas(self, width=600, height=500)
            canvas.grid(row=2, column=2)
            canvas.create_image(200, 200, image=img_gif_2)


    class PageOne(tk.Frame):

        def __init__(self, parent, controller):

            def update_status():

                # Get the current message
                current_status = lab2["text"]

                # If the message is "Working...", start over with "Working"
                if (data_read == False):
                    current_status = " "

                # If not, then just add a "." on the end
                else:
                    current_status = str(curr_val)

                # Update the message
                lab2["text"] = current_status

                # After 1 second, update the status
                self.after(100, update_status)

            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Test Auto Filling", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            button1 = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(page1))
            button1.grid(row=1, column=0, padx=10, pady=5)

            button2 = ttk.Button(self, text="Page Two",
                                 command=lambda: controller.show_frame(PageTwo))
            button2.grid(row=1, column=1, padx=10, pady=5)

            button3 = ttk.Button(self, text="Read",
                                 command=read_once)
            button3.grid(row=2, column=2, padx=10, pady=5)

            lab1 = tk.Label(self, text="My voltage: ")
            lab1.grid(row=2, column=0, padx=10, pady=5)
            lab2 = tk.Label(self, text=" ")
            lab2.grid(row=2, column=1, padx=10, pady=5)
            self.after(100, update_status)

    class PageTwo(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
            label.grid(row=0, column=0, padx=10, pady=5)

            button1 = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(page1))
            button1.grid(row=1, column=0, padx=10, pady=5)

            button2 = ttk.Button(self, text="Page One",
                                 command=lambda: controller.show_frame(PageOne))
            button2.grid(row=1, column=1, padx=10, pady=5)

    class oscilloscope_page(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)

            def clear():
                a.clear()
                a.grid(True)
                global data
                data = []

            label = tk.Label(self, text="Live Plotting!", font=LARGE_FONT)
            label.grid(row=0, column=1, padx=10, pady=5)

            button1 = ttk.Button(self, text="Back to Home",
                                 command=lambda: controller.show_frame(page1))
            button1.grid(row=1, column=1, padx=10, pady=5)

            global data
            data = []
            clear()

            button_c = tk.Button(self, text="Clear Plotting", width=10, command=clear)
            button_c.grid(row=2, column=0, padx=10, pady=5)

            button_s = tk.Button(self, text="Stop Plotting", width=10, command=close)
            button_s.grid(row=2, column=1, padx=10, pady=5)

            button_r = tk.Button(self, text="Resume Plotting", width=10, command=connect)
            button_r.grid(row=2, column=2, padx=10, pady=5)

            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=1, padx=10, pady=5)
            toolbarFrame = Frame(self)
            toolbarFrame.grid(row=4, column=1)
            toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
            toolbar.update()

    app = major()
    start_ani()
    app.mainloop()
