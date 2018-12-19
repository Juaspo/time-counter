'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time

from tkinter import *
from tkinter import messagebox

import main.main_program as mp
import main.computer_control as cc


#import tkinter
#from tkinter import Button
#from tkinter.ttk import Frame

if __name__ == '__main__':
    pass


top = Tk()
top.minsize(width=250, height=150) 
#top.geometry("100x100")
frame = Frame(top)
frame.pack()

mp.initiate_parameters()


def quit():
    if (mp.is_working()):
        MsgBox = messagebox.askyesno("Exit Application","Are you sure you want to exit the application", icon = "warning")
        if (MsgBox):
            mp.stamp_time(4, "user")
            top.destroy()
        else:
            print("Exit aborted")
    else:
        print ("good bye")
        top.destroy()
        
    #msg = messagebox.showinfo("Hi", "Hello World!")


def run_clocking():
    if(mp.is_working()):
        mp.end_clocking("user")
        start_btn.config(text = "Start")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#e00")
    else:
        mp.begin_clocking("user")
        start_btn.config(text = "Stop")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#0e0")
    
    time.sleep(0.05)
    
    
def timestamp():
    action_type = 3
    
    #if in running mode change action to "Running"
    if (mp.is_working()):
        action_type = 2
        
    print ("Timestamp")
    mp.stamp_time(action_type, 0, "Timestamp")
    
    
def goto_sleep():
    print ("going to sleep mode... Good night!")
    label.config(text = "Sleep")
    cc.put_to_sleep()

label = Label(frame, text="Welcome!", fg="black", font="Verdana 30 bold") 
label.pack() 

e1 = Entry(frame, width = 15)
e1.pack()

start_btn = Button(frame, text = "Start", width = 15, command = run_clocking)
start_btn.pack()

stamp_btn = Button(frame, text="Timestamp", width = 15, command = timestamp)
stamp_btn.pack()

sleep_btn = Button(frame, text = "Sleep", width = 15, command = goto_sleep)
sleep_btn.pack()

exit_btn = Button(frame, text="Exit", width = 15, command = quit)
exit_btn.pack()

#btn.place(x=50, y=50)
top.mainloop()