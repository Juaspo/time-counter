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
            mp.stamp_time(4, False, "user")
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
    input = text_entry.get()
    if input =="":
        input = "Timestamp"
    mp.stamp_time(action_type, False, input)
    
    
def goto_sleep():
    print ("going to sleep mode... Good night!")
    label.config(text = "Sleep")
    cc.put_to_sleep()
    
    
def debugging_stuff():
    print ("changing date")
    txt = mp.change_Date()
    label.config(text = txt)

label = Label(frame, text="Welcome!", fg="black", font="Verdana 30 bold") 
label.pack() 



start_btn = Button(frame, text = "Start", font="Verdana 20 bold", width = 10, height = 5, command = run_clocking)
start_btn.pack()

frame2 = Frame(frame)
frame2.pack()

text_entry = Entry(frame2, width = 15)
text_entry.grid(row = 0, column = 0)
#text_entry.pack()

debug_btn = Button(frame, text = "Debugging", width = 15, command = debugging_stuff)
debug_btn.pack()

stamp_btn = Button(frame2, text="Timestamp", width = 15, command = timestamp)
stamp_btn.grid(row = 1, column = 0)
#stamp_btn.pack()

sleep_btn = Button(frame2, text = "Sleep", width = 15, command = goto_sleep)
sleep_btn.grid(row = 0, column = 1)
#sleep_btn.pack()

exit_btn = Button(frame2, text="Exit", width = 15, command = quit)
exit_btn.grid(row = 1, column = 1)
#exit_btn.pack()

#btn.place(x=50, y=50)
top.mainloop()