'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time
import getopt

import os

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import main.main_program as mp
import main.computer_control as cc


import main.file_handler as fh


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
config_file_name = ".config"

def btn0_action():
    check_if_runnung()
    if (alternative_buttons):
        goto_sleep()
    else:
        timestamp()

def btn1_action():
    check_if_runnung()
    if (alternative_buttons):
        shutdown_pc()
    else:
        check_time()

def btn2_action():
    check_if_runnung()
    if (alternative_buttons):
        quit_func()
    else:
        debugging_stuff()


def btn3_action():
    check_if_runnung()
    change_buttons()

def config_reset_action():
    restore_data = fh.read_data(config_file_name)
    config_values = []
    
    for config_value in iter(restore_data.splitlines()):
        config_values.append(config_value)
        
    
    if restore_data is not None:
        try:
            text_entry_work_duration.delete(0, END)
            text_entry_work_duration.insert(0, config_values[0])
            hard_limit_text_entry.delete(0, END)
            hard_limit_text_entry.insert(0, config_values[1])
            soft_limit_text_entry.delete(0, END)
            soft_limit_text_entry.insert(0, config_values[2])
            shutdown_delay_text_entry.delete(0, END)
            shutdown_delay_text_entry.insert(0, config_values[3])
            new_start_time_entry.delete(0, END)
            new_start_time_entry.insert(0, config_values[4])
        except IndexError:
            print("Incomplete config file")
        
        
    else:
        print("No config found")
        

def set_new_start_time():
    try:
        new_time = mp.time_conversion(new_start_time_entry.get(), True)
        print("New start time:", new_time, "\nfrom:", new_start_time_entry.get())
        mp.set_start_time(new_time)
    except ValueError:
        print("New start time not a number")


def set_limits(soft_l, hard_l):
    try:
        mp.set_soft_delay_limit(int(soft_l))
    except ValueError:
        print("Soft limit not a number")
    
    try:
        mp.set_time_delay_limit(int(hard_l))
    except ValueError:
        print("Hard limit not a number")
    


def config_save_action():
    textentry = text_entry_work_duration.get()
    textentry += "\n" + hard_limit_text_entry.get()
    textentry += "\n" + soft_limit_text_entry.get()
    textentry += "\n" + shutdown_delay_text_entry.get()
    textentry += "\n" + new_start_time_entry.get()
    
    fh.write_data_to_file(config_file_name, "w", textentry)
    set_limits(soft_limit_text_entry.get(), hard_limit_text_entry.get())


def quit_func():
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
        label.config(text = "Aborted!")
        os.system("shutdown /a")
        shutdown_sequence = False
        btn1["text"] = "Shutdown PC"
        check_if_runnung()
        
    else:
        print ("Shutting down PC Good bye!")
        label.config(text = "Shutdown!", bg="#d00", fg="#000")
        
        if (mp.is_working()):
            mp.end_clocking(4, "user")
        
        
        try:
            int(shutdown_delay_text_entry.get())
            shutdown_time = shutdown_delay_text_entry.get()
        except ValueError:
            shutdown_time = "40"
            print("Shutdown time not a number! Default 40s set")
            
        
        print (shutdown_time, "secs to shutdown")
        sequence = "shutdown /s /t " + shutdown_time + " /c \"Time counter shutdown\" /f /d p:0:0"
        print("seq", sequence)
        #os.system("shutdown /s /t 40 /c \"Time counter shutdown\" /f /d p:0:0")
        os.system(sequence)
        
        shutdown_sequence = True
        btn1["text"] = "Abort Shutdown"
    
def clear_field():
    print("clear input field")

def run_end_clocking(msg = None):
    if msg is None:
        msg = "user"
        
    if(mp.is_working()):
        mp.end_clocking(0, msg)
        start_btn.config(text = "Start")
        txt = mp.time_value_content()
        label.config(text = txt)
    else:
        mp.begin_clocking(msg)
        start_btn.config(text = "Stop")
        txt = mp.time_value_content()
        label.config(text = txt, fg="#000")
    
    time.sleep(0.05)
    check_if_runnung()
    
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
    #print ("placeholder")
    check_if_runnung()
    current_time = mp.convert_to_time(mp.time_conversion(mp.get_time()))
    text_entry_end.delete(0, END)
    text_entry_end.insert(0, current_time)

def check_if_runnung():
    if mp.is_working():
        label.config(bg="#9e9")
        start_btn.config(text = "Stop")
    else:
        label.config(bg="#e99")
        start_btn.config(text = "Start")

def check_time():
    check_if_runnung()
    
    config_time_value = 0
    old_time_value = 0
    time_duration = 0
    if mp.is_working():
        try:
            fetch_config_time_value = mp.time_conversion(text_entry_work_duration.get(), True)
            time_duration = mp.get_time_value() - mp.get_start_time()
            
            config_time_value = fetch_config_time_value - time_duration
            time_left = mp.convert_to_time(abs(config_time_value))
            
            if(config_time_value <= 0):
                label.config(text = time_left, fg="#070")
                
            else:
                label.config(text = time_left, fg="#700")
             
            '''   
            #wait 1s and display start time again
            temp_timer = mp.get_time_value()
            while (temp_timer+2 < mp.get_time_value()):
                pass
            label.config(text = mp.convert_to_time(mp.get_start_time()))
            '''
                
        except ValueError:
            print("wrong format")
        
        
        #print("debug time left: ", time_left, " duration: ", time_duration)
    else:
        print("timer not running!")
        label.config(text = "no run!", fg="#000")
    

def change_buttons():
    global alternative_buttons
    
    #First set of buttons
    if (alternative_buttons):
        btn0["text"] = "Timestamp"
        btn1["text"] = "Check time"
        btn2["text"] = "Starting time"
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
    label.config(text = mp.convert_to_time(mp.get_start_time()), fg="#000")
    #print ("write recovery")
    #txt = mp.change_Date()
    
    #txt = mp.change_time()
    #label.config(text = mp.convert_to_time(txt))
    
    
    #text_entry_start.insert(0, "12:05:15")
    #text_entry_end.insert(0, "12:15:35")
    #mp.convert_to_ericsson_time("07:59:01")
    
    
def debugging_stuff2():
    pass
    #print ("write recovery")
    #txt = mp.change_Date()
    
    #txt = mp.change_time()
    #label.config(text = mp.convert_to_time(txt))
    
    #text_entry_start.insert(0, "12:05:15")
    #text_entry_end.insert(0, "12:15:35")
    #mp.convert_to_ericsson_time("07:59:01")
    
    
label = Label(main_frame1, text="Beast!", fg="black", font="Verdana 30 bold") 
label.pack() 

start_btn = Button(main_frame1, text = "Start", font="Verdana 20 bold", width = 10, height = 5, command = run_end_clocking)
start_btn.pack()

text_entry = Entry(main_frame2, width = 15)
text_entry.grid(row = 0, column = 0)
#text_entry.pack()

btn3 = Button(main_frame0, text = "2nd", width = 15, command = change_buttons)
btn3.pack()

btn0 = Button(main_frame2, text="Timestamp", width = 15, command = btn0_action)
btn0.grid(row = 0, column = 1)
#btn0.pack()

btn1 = Button(main_frame2, text = "Check time", width = 15, command = btn1_action)
btn1.grid(row = 1, column = 0)
#btn1.pack()

btn2 = Button(main_frame2, text="Starting time", width = 15, command = btn2_action)
btn2.grid(row = 1, column = 1)
#btn2.pack()

text_entry_start = Entry(conv_frame2, width = 15)
text_entry_start.grid(row = 0, column = 0)

text_entry_end = Entry(conv_frame2, width = 15)
text_entry_end.grid(row = 1, column = 0)

diff_btn = Button(conv_frame2, text="Calculate", width = 15, command = get_time_difference)
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




###################### Configuration Pane
work_hours_label = Label(config_frame0, anchor = "w", text="Work hours", fg="black", width = 15) 
work_hours_label.grid(row = 0, column = 0)

text_entry_work_duration = Entry(config_frame0, width = 15)
text_entry_work_duration.grid(row = 0, column = 1)
#text_entry_work_duration.insert(1.0, "--:--")

hard_limit_label = Label(config_frame0, anchor = "w", text="Hard limit time", fg="black", width = 15) 
hard_limit_label.grid(row = 1, column = 0)

hard_limit_text_entry = Entry(config_frame0, width = 15)
hard_limit_text_entry.grid(row = 1, column = 1)

soft_limit_label = Label(config_frame0, anchor = "w", text="Soft limit time", fg="black", width = 15) 
soft_limit_label.grid(row = 2, column = 0)

soft_limit_text_entry = Entry(config_frame0, width = 15)
soft_limit_text_entry.grid(row = 2, column = 1)

shutdown_delay_label = Label(config_frame0, anchor = "w", text="Shutdown delay", fg="black", width = 15) 
shutdown_delay_label.grid(row = 3, column = 0)

shutdown_delay_text_entry = Entry(config_frame0, width = 15)
shutdown_delay_text_entry.grid(row = 3, column = 1)

new_start_time_button = Button(config_frame0, text="Set start time", width = 15, command = set_new_start_time) 
new_start_time_button.grid(row = 4, column = 0)

new_start_time_entry = Entry(config_frame0, width = 15)
new_start_time_entry.grid(row = 4, column = 1)

config_reset_btn = Button(config_frame0, text="Reset", width = 15, command = config_reset_action)
config_reset_btn.grid(row = 6, column = 0)
config_save_btn = Button(config_frame0, text="Save", width = 15, command = config_save_action)
config_save_btn.grid(row = 6, column = 1)


mp.initiate_parameters()
    
def main(argv):
    global take_timestamp
    global autostart
    
    mp.check_and_restore()
    config_reset_action()
    set_limits(soft_limit_text_entry.get(), hard_limit_text_entry.get())
    
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
            run_end_clocking(arg)
            autostart = True
            
        print ("auto start:", autostart, "timestamp:", take_timestamp, "argv:", argv, "opts:", opts)

if __name__ == '__main__':
    main(sys.argv[1:])

#btn.place(x=50, y=50)
top.mainloop()
