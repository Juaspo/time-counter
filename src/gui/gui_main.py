'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time
import sys, getopt

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import main.main_program as mp
import main.computer_control as cc
from _overlapped import NULL


#import tkinter
#from tkinter import Button
#from tkinter.ttk import Frame

autostart = False
take_timestamp = False


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

#top.geometry("100x100")
frame = Frame(tab1)
frame.pack()

frame1 = Frame(frame)
frame1.pack()

frame21 = Frame(tab2)
frame21.pack()

frame2 = Frame(frame)
frame2.pack()

frame3 = Frame(tab2)
frame3.pack()





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


def run_clocking(msg = None):
    if msg is None:
        msg = "user"
        
    if(mp.is_working()):
        mp.end_clocking(msg)
        start_btn.config(text = "Start")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#e00")
    else:
        mp.begin_clocking(msg)
        start_btn.config(text = "Stop")
        txt = mp.time_value_content()
        label.config(text = txt, bg="#0e0")
    
    time.sleep(0.05)
    
    
def timestamp(msg = None):
    action_type = 3
    
    #if in running mode change action to "Running"
    if (mp.is_working()):
        action_type = 2
        
    print ("Timestamp")
    if msg is None:
        input = text_entry.get()
        if input =="":
            input = "Timestamp"
    else:
        input = msg
    mp.stamp_time(action_type, False, input)
    
    
def goto_sleep():
    print ("going to sleep mode... Good night!")
    label.config(text = "Sleep")
    cc.put_to_sleep()
    
    
def get_time_difference():
    
    input_start = mp.time_conversion(text_entry_start.get(), True)
    input_end = mp.time_conversion(text_entry_end.get(), True)
    
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
    
    
def debugging_stuff():
    print ("changing date")
    #txt = mp.change_Date()
    #txt = mp.change_time()
    #label.config(text = txt)
    text_entry_start.insert(0, "12:05:15")
    text_entry_end.insert(0, "12:15:35")
    #mp.convert_to_ericsson_time("07:59:01")
    
    
label = Label(frame1, text="Welcome!", fg="black", font="Verdana 30 bold") 
label.pack() 

start_btn = Button(frame1, text = "Start", font="Verdana 20 bold", width = 10, height = 5, command = run_clocking)
start_btn.pack()

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


text_entry_start = Entry(frame3, width = 15)
text_entry_start.grid(row = 0, column = 0)

text_entry_end = Entry(frame3, width = 15)
text_entry_end.grid(row = 1, column = 0)

diff_btn = Button(frame3, text="calculate", width = 15, command = get_time_difference)
diff_btn.grid(row = 0, column = 1)

label_etime = Label(frame3, text="Welcome!", fg="black") 
label_etime.grid(row = 1, column = 1)

work_duration_label = Label(frame21, anchor = "w", text="Work duration", fg="black", width = 15) 
work_duration_label.grid(row = 0, column = 0)

ericsson_time_label = Label(frame21, anchor = "w", text="Ericsson time", fg="black", width = 15) 
ericsson_time_label.grid(row = 1, column = 0)


duration_result_label = Text(frame21, height = 1, borderwidth = 0, width = 15) 
duration_result_label.insert(1.0, "--:--:--")
duration_result_label.grid(row = 0, column = 1)
duration_result_label.configure(state="disabled")

ericsson_result_label = Text(frame21, height = 1, borderwidth = 0, width = 15)
ericsson_result_label.insert(1.0, "--:--")
ericsson_result_label.grid(row = 1, column = 1)
ericsson_result_label.configure(state="disabled")

mp.initiate_parameters()
    
def main(argv):
    global take_timestamp
    global autostart
    
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
