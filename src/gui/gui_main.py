'''
Created on 23 nov. 2018

@author: ezasaju
'''

from tkinter import *
from tkinter import messagebox
from main import main_program
from main import computer_control


#import tkinter
#from tkinter import Button
#from tkinter.ttk import Frame

if __name__ == '__main__':
    pass

mp = main_program
cc = computer_control

top = Tk()
top.minsize(width=250, height=100) 
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
    print ("start clocking")
    label.config(text = "Clocking")
    mp.begin_clocking("user")
    
    
def stop_clocking():
    print ("end clocking")
    label.config(text = "Stopped")
    mp.end_clocking("user")

label = Label(frame, text="Welcome!", fg="black", font="Verdana 30 bold") 
label.pack() 

btn = Button(frame, text = "Start", width = 15, command = run_clocking)
btn.pack()

b = Button(frame, text="End", width = 15, command = stop_clocking)
b.pack()

b = Button(frame, text="Exit", width = 15, command = quit)
b.pack()

#btn.place(x=50, y=50)
top.mainloop()

#computer_control.put_to_sleep()