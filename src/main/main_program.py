'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time
import os
import threading

#from main import thread_handler

time_array = []


test_nr = 0
temp_date = 0
date = 0
day = "No_day"
temp_time_value = 0
time_value = 0
start_time = 0
month = ""
int_month = 0
year = 0
same_day = 1
working = 0
file_name = ""
log_intro = ""
id_number = ""
action_mode = ("Stopped", "Started", "Running", "No data")

debug_test_variable = 0

sleep_time = 2

debug_counter = 0

#max allowed time passed between checks to not trigger sleep mode
time_delay_limit = 10


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        
    def stop(self):
        print("stopping thread...")
        self._stop_event.set()

    def stopped(self):
        print("thread stopped?", self._stop_event.is_set())
        return self._stop_event.is_set()
    
    def run(self):
        print("Thread running!")
        
        while (not self.stopped()):
            running("Kimpa")
            time.sleep(1)
            

counterThread = StoppableThread()
counterThread.setDaemon(True)


#test print for debug purpose
def test_case(msg = ""):
    global test_nr
    global temp_time_value
    global time_value
    global temp_date
    global date
    
    print ("\n", msg, "test#", test_nr, "\nday:", day, "temp_date:", temp_date, "date:", date, "temp_time:", temp_time_value, "time:", time_value, "\nTime array:")
    test_nr += 1
    for x in time_array:
        print (x)
    print("\n")

def initiate_parameters():
    global date
    global day
    global month
    global year
    global time_value
    global temp_time_value
    global time_array
    global same_day
    global file_name
    global log_intro
    #global id_number
    global int_month
    global counterThread
    
    day = time.strftime("%a")
    date = get_date()
    month = time.strftime("%b")
    int_month = time.strftime("%m")
    year = time.strftime("%Y")
    log_intro = "Log file: " + str(date).zfill(2) + " " + month + " " + year + "\n"
    file_name = "logTime_" + str(int_month).zfill(2) + "-" + str(year) + ".txt"
    time_value = time_conversion(get_time())
    same_day = 0;
    


#Converts time to a decimal number between 0 (00:00:00) and 86399 (23:59:59)
def time_conversion(t):
    global debug_counter
    global debug_test_variable
    global time_value
    
    return (t[0]*3600+t[1]*60+t[2])


def get_time():
    t = [int(time.strftime("%H")), int(time.strftime("%M")), int(time.strftime("%S"))] 
    return t

#Takes in time as decimal and returns time value as string
def convert_to_time(t):
    h=0
    m=0
    s=0
    str_time = ""
    
    h=int(t/3600)
    m=int((t-h*3600)/60)
    s=t-h*3600-m*60
    str_time = (str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2))
    
    print ("time t:", t, "converts to:", str_time)
    return str_time

def store_time_date(action, msg, work_time = "--:--:--"):
    global date
    global day
    global month
    global year
    global time_array
    global time_value
    global id_number
    
    data_to_store = ""
    data_to_store = day + "\t" + str(date) + "/" + month + "/" + str(year) + "\t" + id_number + "\t" + convert_to_time(time_value) + "\t" + work_time + "\t" + action_mode[action] + "\t" + msg
    
    print("id:", id_number)
    time_array.append(data_to_store)
    log_to_file(data_to_store)

def get_time_diff(current_time_value, saved_time_value):
    if current_time_value < saved_time_value:
        return convert_to_time((current_time_value + 86400) - saved_time_value)
    else:
        return convert_to_time(current_time_value - saved_time_value)


def begin_clocking(msg = ""):
    global working
    global id_number
    global date
    global int_month
    global start_time
    global temp_time_value
    global time_value
    
    if working == 0:
        initiate_parameters()
        start_time = time_value
        id_number = str(date) + str(int_month).zfill(2) + str(time_value)
        working = 1
        try:
            counterThread.start()
            store_time_date(1, msg)
            #threading.Thread(target=running).start()
        except:
            print ("Error: unable to start thread")
        return True
        
    else:
        stamp_time(2, msg)
        return False
    
    
    
def end_clocking(msg = ""):
    global working
    global time_value
    global temp_time_value
    global counterThread
    
    if working != 0:
        working = 0
        stamp_time(0, msg)
        
        counterThread.stop()
        counterThread.join()
        
        counterThread = StoppableThread()
        counterThread.setDaemon(True)
        return True
        
    else:
        stamp_time(3, msg)
        return False
    
def onExit():
    if counterThread.isAlive()==True:
        print("thread is running still")
        counterThread.stop()
    else:
        print("thread is running terminated")

def stamp_time(action, msg):
    work_time = ""
    work_time = get_time_diff(temp_time_value, start_time)
    store_time_date(action, msg, work_time)
    

def get_date():
    return int(time.strftime("%d"))


def new_day():
    global date
    global temp_date
    global day
    global time_value
    global temp_time_value
    global working
    
    time_value_adjustment = 86400 #86400 for 24h next day adjustment
    
    day = time.strftime("%a")
    temp_time_value = time_conversion(get_time())
    
    #New day confirmed so check if limit passed over 23:59-00:00 mark
    if temp_time_value + time_value_adjustment > (time_value + time_delay_limit):
        stamp_time(0, "timeout")
        working = 0;
        begin_clocking("new-day")
        #date = temp_date #remove this (debug stuff)
        
    else:
        #print("No limit passed ::new day:: time difference:", temp_time_value+time_value_adjustment-time_value, "tmp", temp_time_value, "time:", time_value, "debug nr:", debug_counter)
        time_value = temp_time_value
        date = temp_date
        

def check_date():
    global temp_date
    global date
    global same_day
    temp_date = get_date()
        
    if date != temp_date:
        new_day()
        return (0)
    return(1)


def check_time():
    global temp_time_value
    global time_value
    global time_delay_limit
    global working
    
    temp_time_value = time_conversion(get_time())
    
    #check if time now (temp_time_value) is greater than last checked time
    if temp_time_value > time_value:
        #check if time now exceed time delay limit for time check
        if temp_time_value > (time_value + time_delay_limit):
            #Delay is more than timeout approved delay
            stamp_time(0, "timeout")
            begin_clocking()
            time_value = temp_time_value
        
        #time is within time check delay limit
        else:
            #update time_value to current time
            time_value = temp_time_value
    
    #Somehow temp_time_value is less than time_value which should be handled by new day so something is wrong if this is entered
    else:
        print ("Something went wrong!", time_value, "new", temp_time_value)
        

#Loop of regular checks if system is still active
def running(threadName = "Kim"):
    global sleep_time
    global debug_counter
    global working
    
    if(check_date()):
        check_time()
    debug_counter += 1
    

def log_to_file(s):
    # Open a file
    global file_name
    
    print("File!!", file_name, "content:", s)
    fo = open(file_name, "a")
    
    if os.stat(file_name).st_size == 0:
        fo.write(log_intro)
        fo.write("day\tdate\t\tid number\ttime\t\twork time\taction\tmessage\n")
    
    fo.write(s + "\n")
    fo.close()
    
'''
def init_program():
    initiate_parameters()
    x = ""
    
    while x != "q":
        print("Welcome to TimeCounter. Choose option: 1:Start counter 2:Stop Counter 3:Show Time Q:Exit ")
        x = input("#:")
        if x == "1":
            start_thread()
        elif x == "2":
            print("value of x:", x)
            end_clocking()
        else:
            print("value of x:", x)

#init_program()

#next to fix is to add save of timestamps-

'''