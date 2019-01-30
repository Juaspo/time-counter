'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time
import sys, getopt

import os

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import main.main_program as mp
import main.computer_control as cc

from _overlapped import NULL
from pip._vendor.html5lib import _inputstream



#import tkinter
#from tkinter import Button
#from tkinter.ttk import Frame

autostart = False
take_timestamp = False
shutdown_sequence = False



top = Tk()
top.minsize(width=250, height=150)

top.title("Time counter")

tabControl = ttk.Notebook(top)          # Create Tab Control
tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Main')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible
tab2 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab2, text='Conversion')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible
tab3 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab3, text='Configuration')      # Add the tab
tabControl.pack(expand=1, fill="both")  # Pack to make visible

#top.geometry("100x100")
main_frame0 = Frame(tab1)
main_frame0.pack()

main_frame1 = Frame(main_frame0)
main_frame1.pack()

main_frame2 = Frame(main_frame0)
main_frame2.pack()

conv_frame1 = Frame(tab2)
conv_frame1.pack()

conv_frame2 = Frame(tab2)
conv_frame2.pack()

config_frame0 = Frame(tab3)
config_frame0.pack()


alternative_buttons = False


def btn0_action():
    if (alternative_buttons):
        goto_sleep()
    else:
        timestamp()

def btn1_action():
    if (alternative_buttons):
        shutdown_pc()
    else:
        debugging_stuff2()

def btn2_action():
    if (alternative_buttons):
        quit()
    else:
        debugging_stuff()


def btn3_action():
    change_buttons()

def config_reset_action():
    pass

def config_save_action():
    pass


def quit():
    if (mp.is_working()):
        MsgBox = messagebox.askyesno("Exit Application","Are you sure you want to exit the application", icon = "warning")
        if (MsgBox):
            mp.end_clocking(4, "user")
            top.destroy()
        else:
            print("Exit aborted")
    else:
        print ("good bye")
        top.destroy()
        
    #msg = messagebox.showinfo("Hi", "Hello World!")


def shutdown_pc():
    global shutdown_sequence
    
    if (shutdown_sequence):
        print ("Shutdown Aborted!")
        label.config(text = "Aborted!", bg="#0e0")
        os.system("shutdown /a")
        shutdown_sequence = False
        btn1["text"] = "Shutdown PC"
        
    else:
        print ("Shutting down PC Good bye!")
        label.config(text = "Shutdown!", bg="#e00")
        if (mp.is_working()):
            mp.stamp_time(4, False, "user")
        print ("40 secs to shutdown")
        os.system("shutdown /s /t 40 /c \"Time counter shutdown\" /f /d p:0:0")
        shutdown_sequence = True
        btn1["text"] = "Abort Shutdown"
    
def clear_field():
    print("clear input field")

def run_clocking(msg = None):
    if msg is None:
        msg = "user"
        
    if(mp.is_working()):
        mp.end_clocking(0, msg)
        start_btn.config(text = "Start")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#e99")
    else:
        mp.begin_clocking(msg)
        start_btn.config(text = "Stop")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#9e9")
    
    time.sleep(0.05)
    
    
def timestamp(msg = None):
    action_mode = 3
    
    #if in running mode change action to "Running"
    if (mp.is_working()):
        action_mode = 2
        
    print ("Timestamp")
    if msg is None:
        input = text_entry.get()
        if input =="":
            input = "Timestamp"
    else:
        input = msg
    mp.stamp_time(action_mode, False, input)
    
    
def goto_sleep():
    print ("going to sleep mode... Good night!")
    label.config(text = "Sleep")
    cc.put_to_sleep()
    
    
def get_time_difference():
    
    input_start = mp.time_conversion(text_entry_start.get(), True)
    input_end = mp.time_conversion(text_entry_end.get(), True)
    
    text_entry_start.delete(0, END)
    text_entry_end.delete(0, END)
    text_entry_start.insert(0, mp.convert_to_time(input_start))
    text_entry_end.insert(0, mp.convert_to_time(input_end))
    
    print("Get time diff", input_start, input_end)
    
    if input_start is None:
        text_entry_start.config(fg = "red")
    elif input_end is None:
        text_entry_end.config(fg = "red")
    else:
        text_entry_end.config(fg = "black")
        text_entry_start.config(fg = "black")
        
        result = mp.get_time_diff(input_start, input_end)
        eresult = mp.convert_to_ericsson_time(result)
    
        duration_result_label.configure(state="normal")
        duration_result_label.delete(1.0, END)
        duration_result_label.insert(1.0, result)
        duration_result_label.configure(state="disabled")
        
        ericsson_result_label.configure(state="normal")
        ericsson_result_label.delete(1.0, END)
        ericsson_result_label.insert(1.0, eresult)
        ericsson_result_label.configure(state="disabled")

def get_current_time():
    print ("placeholder")
    current_time = mp.convert_to_time(mp.time_conversion(mp.get_time()))
    text_entry_end.delete(0, END)
    text_entry_end.insert(0, current_time)
    

def change_buttons():
    global alternative_buttons
    
    #First set of buttons
    if (alternative_buttons):
        btn0["text"] = "Timestamp"
        btn1["text"] = "Clear"
        btn2["text"] = "Debug"
        btn3["text"] = "2nd"
        text_entry.configure(state="normal")
        alternative_buttons = False
        
    #Second set of buttons
    else:
        btn0["text"] = "Sleep"
        if (shutdown_sequence):
            btn1["text"] = "Abort Shutdown"
        else:
            btn1["text"] = "Shutdown PC"
        btn2["text"] = "Exit"
        btn3["text"] = "1st"
        text_entry.configure(state="disabled")
        alternative_buttons = True
        
    
def debugging_stuff():
    print ("write recovery")
    #txt = mp.change_Date()
    
    #txt = mp.change_time()
    #label.config(text = mp.convert_to_time(txt))
    
    
    #text_entry_start.insert(0, "12:05:15")
    #text_entry_end.insert(0, "12:15:35")
    #mp.convert_to_ericsson_time("07:59:01")
    
    
def debugging_stuff2():
    print ("write recovery")
    #txt = mp.change_Date()
    
    #txt = mp.change_time()
    #label.config(text = mp.convert_to_time(txt))
    
    print("retrieved: ")
    
    #text_entry_start.insert(0, "12:05:15")
    #text_entry_end.insert(0, "12:15:35")
    #mp.convert_to_ericsson_time("07:59:01")
    
    
label = Label(main_frame1, text="Beast!", fg="black", font="Verdana 30 bold") 
label.pack() 

start_btn = Button(main_frame1, text = "Start", font="Verdana 20 bold", width = 10, height = 5, command = run_clocking)
start_btn.pack()

text_entry = Entry(main_frame2, width = 15)
text_entry.grid(row = 0, column = 0)
#text_entry.pack()

btn3 = Button(main_frame0, text = "2nd", width = 15, command = change_buttons)
btn3.pack()

btn0 = Button(main_frame2, text="Timestamp", width = 15, command = btn0_action)
btn0.grid(row = 0, column = 1)
#btn0.pack()

btn1 = Button(main_frame2, text = "DB2", width = 15, command = btn1_action)
btn1.grid(row = 1, column = 0)
#btn1.pack()

btn2 = Button(main_frame2, text="Debug", width = 15, command = btn2_action)
btn2.grid(row = 1, column = 1)
#btn2.pack()

text_entry_start = Entry(conv_frame2, width = 15)
text_entry_start.grid(row = 0, column = 0)

text_entry_end = Entry(conv_frame2, width = 15)
text_entry_end.grid(row = 1, column = 0)

diff_btn = Button(conv_frame2, text="calculate", width = 15, command = get_time_difference)
diff_btn.grid(row = 0, column = 1)

get_time_btn = Button(conv_frame2, text="Current time", width = 15, command = get_current_time)
get_time_btn.grid(row = 1, column = 1)

#label_etime = Label(conv_frame2, text="Welcome!", fg="black") 
#label_etime.grid(row = 1, column = 1)

work_duration_label = Label(conv_frame1, anchor = "w", text="Work duration", fg="black", width = 15) 
work_duration_label.grid(row = 0, column = 0)

ericsson_time_label = Label(conv_frame1, anchor = "w", text="Ericsson time", fg="black", width = 15) 
ericsson_time_label.grid(row = 1, column = 0)


duration_result_label = Text(conv_frame1, height = 1, borderwidth = 0, width = 15) 
duration_result_label.insert(1.0, "--:--:--")
duration_result_label.grid(row = 0, column = 1)
duration_result_label.configure(state="disabled")

ericsson_result_label = Text(conv_frame1, height = 1, borderwidth = 0, width = 15)
ericsson_result_label.insert(1.0, "--:--")
ericsson_result_label.grid(row = 1, column = 1)
ericsson_result_label.configure(state="disabled")


text_entry_work_duration = Entry(config_frame0, width = 15)
text_entry_work_duration.grid(row = 0, column = 1)
#text_entry_work_duration.insert(1.0, "--:--")

ericsson_time_label = Label(config_frame0, anchor = "w", text="Work duration", fg="black", width = 15) 
ericsson_time_label.grid(row = 0, column = 0)


config_reset_btn = Button(config_frame0, text="Reset", width = 15, command = config_reset_action)
config_reset_btn.grid(row = 3, column = 0)
config_save_btn = Button(config_frame0, text="Save", width = 15, command = config_save_action)
config_save_btn.grid(row = 3, column = 1)


mp.initiate_parameters()
    
def main(argv):
    global take_timestamp
    global autostart
    
    mp.check_and_restore()
    
    try:
        opts, args = getopt.getopt(argv, "hs:t:", ["help"])
    except getopt.GetoptError:
        print("Wrong input try -h for help")
        sys.exit(2)
    
    for opt, arg in opts:
        print("arg:", arg)
        if opt in ("-h", "--help"):
            print("\nTimeCounter help screen\n")
            print("-h\tfor this help text\n-s\tfor auto start\n-t\tfor timestamp")
            sys.exit()
        elif opt == "-t":
            timestamp(arg)
            take_timestamp = True
        elif opt == "-s":
            run_clocking(arg)
            autostart = True
            
        print ("auto start:", autostart, "timestamp:", take_timestamp, "argv:", argv, "opts:", opts)

if __name__ == '__main__':
    main(sys.argv[1:])

#btn.place(x=50, y=50)
top.mainloop()
