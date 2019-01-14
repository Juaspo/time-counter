'''
Created on 23 nov. 2018

@author: ezasaju
'''
import time
import threading
import re
import main.file_handler as fh


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
id_number = "000000000"
action_mode = ("Stopped", "Started", "Running", "No data", "Aborted", "Recover")
ericsson_time = 0
recovery_file_name = ".data"

debug_test_variable = 0
recovery_interval = 10
sleep_time = 2

debug_counter = 0

#max allowed time passed between checks to not trigger sleep mode
time_delay_limit = 9000
soft_delay_limit = 30

#debug function
def change_Date():
    global date
    date = date - 1
    return date

#debug funktion
def change_time():
    global date
    global start_time
    global time_value
    
    time_value -= 300
    return start_time

#Check if periodic checks is running
def is_working():
    return working

def time_value_content():
    return convert_to_time(time_value)


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
        return self._stop_event.is_set()
    
    def run(self):
        global working
        
        working = 1
        delay_counter = 0
        print("Thread running!")
        while (not self.stopped()):
            
            running("Kimpa")
            
            if(delay_counter > recovery_interval):
                recovery_stamp_time()
                delay_counter = 0
            
            time.sleep(1)
            delay_counter += 1
            
        working = 0
            

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
    global int_month
    global counterThread
    global start_time
    
    
    day = time.strftime("%a")
    date = get_date()
    month = time.strftime("%b")
    int_month = time.strftime("%m")
    year = time.strftime("%Y")
    log_intro = "Log file: " + str(date).zfill(2) + " " + month + " " + year + "\nday\tdate\t\tid number\ttime\t\twork time\tE///\taction\tmessage\n"
    time_value = time_conversion(get_time())
    start_time = time_value
    same_day = 0;
    
    file_name = "logTime_" + str(int_month).zfill(2) + "-" + str(year) + ".txt"
    if fh.file_empty(file_name):
        fh.write_data_to_file(file_name, "a", log_intro)
    



def convert_to_ericsson_time(time_in):
    #get time as string and split it up as separate ints
    k = [int(s) for s in re.findall(r'\b\d+\b', time_in)]
    hr = k[0]
    min = k[1]
    sec = k[2]
    
    if sec>30:
        min+=1
    
    min = int(round(min/60*100, 0))
    if min == 100:
        hr += 1
        min = 0
    
    #Add trailing zero if value less than 10 for uniform output
    etime = str(hr) + "," + str(min).zfill(2)
    return etime
    

#Converts time to a decimal number between 0 (00:00:00) and 86399 (23:59:59)
def time_conversion(t, is_string = False):
    t2 = []
    
    if is_string is True:
        t2 = [int(s) for s in re.findall(r'\b\d+\b',t)]
    else:
        t2 = t
        
    while(len(t2) < 3):
        t2.append(0)
        
    #print(t2)
    return (t2[0]*3600+t2[1]*60+t2[2])

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
    return str_time

def store_time_date(action, msg, add_newline, work_time = "--:--:--"):
    global date
    global day
    global month
    global year
    global time_array
    global time_value
    global id_number
    global ericsson_time
    
    if work_time == "--:--:--":
        ericsson_time = "--:--"
    else:
        ericsson_time = convert_to_ericsson_time(work_time)
    
    data_to_store = ""
    data_to_store = day + "\t" + str(date) + "/" + month + "/" + str(year) + "\t" + id_number + "\t" + convert_to_time(time_value) + "\t" + work_time + "\t" + ericsson_time + "\t" + action_mode[action] + "\t" + msg
    if add_newline:
        data_to_store = data_to_store + "\n"
    
    time_array.append(data_to_store)
    return data_to_store

def get_time_diff(saved_time_value, current_time_value):
    if current_time_value < saved_time_value:
        return convert_to_time((current_time_value + 86400) - saved_time_value)
    else:
        return convert_to_time(current_time_value - saved_time_value)


def begin_clocking(msg = ""):
    global working
    global id_number
    global date
    global int_month
    global temp_time_value
    global time_value
    
    initiate_parameters()
    
    id_number = str(date) + str(int_month).zfill(2) + str(time_value)
    s = store_time_date(1, msg, True)
    fh.write_data_to_file(file_name, "a", s)
    
    if not counterThread.isAlive():
        try:
            counterThread.start()
            #threading.Thread(target=running).start()
        except:
            print ("Error: unable to start thread")
        return True
    else:
        print ("Thread already running")
    
    
def end_clocking(action_mode, msg = ""):
    global working
    global time_value
    global temp_time_value
    global counterThread
    
    if working != 0:
        stamp_time(action_mode, False, msg)
        
        counterThread.stop()
        counterThread.join()
        
        counterThread = StoppableThread()
        counterThread.setDaemon(True)
        fh.delete_data_file(recovery_file_name)
        
        return True
        
    else:
        stamp_time(3, False, msg)
        return False
    
def onExit():
    if counterThread.isAlive()==True:
        print("thread is running still")
        counterThread.stop()
    else:
        print("thread terminated")
        
def get_work_time():
    return get_time_diff(start_time, temp_time_value)

def stamp_time(action_m, timeout, msg = ""):
    s = ""
    
    if (id_number == "000000000"):
        s = store_time_date(action_m, msg, True)
    
    else:
        if timeout:
            temp_time_value = time_value
        else:
            temp_time_value = time_conversion(get_time())
            
        
        s = store_time_date(action_m, msg, True, get_work_time())
    
    fh.write_data_to_file(file_name, "a", s)

def get_date():
    return int(time.strftime("%d"))

def new_day():
    global date
    global temp_date
    global day
    global time_value
    global temp_time_value
    global working
    
    time_value_adjustment = (temp_date - date) * 86400 #86400 for 24h adjustment times number of days between current and last check
    day = time.strftime("%a") #update day for log
    temp_time_value = time_conversion(get_time())
    
    #print("temmp", temp_time_value, "time adju:", time_value_adjustment, "time_value", time_value, "delay", time_delay_limit)
    #print("if result:", str((temp_time_value + time_value_adjustment)), "and:", str((time_value + time_delay_limit)))
    #New day confirmed so check if limit passed over 23:59-00:00 mark
    if (temp_time_value + time_value_adjustment) > (time_value + time_delay_limit):
        stamp_time(0, True, "timeout")
        begin_clocking("new-day")
        #date = temp_date #remove this (debug stuff)
        
    elif(temp_time_value + time_value_adjustment) > (time_value + soft_delay_limit):
        stamp_time(2, True, "soft timeout")
        time_value = temp_time_value
        date = temp_date
        stamp_time(2, False, "new-day soft timeout")
        
    else:
        #print("No limit passed ::new day:: time difference:", temp_time_value+time_value_adjustment-time_value, "tmp", temp_time_value, "time:", time_value, "debug nr:", debug_counter)
        time_value = temp_time_value
        date = temp_date
        

def check_date():
    global temp_date
    global date
    global same_day
    temp_date = get_date()
    
    if temp_date != date:
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
    if temp_time_value >= time_value:
        #check if time now exceed time delay limit for time check
        if temp_time_value > (time_value + time_delay_limit):
            #Delay is more than timeout approved delay
            stamp_time(0, True, "timeout")
            begin_clocking("Rerun")
            time_value = temp_time_value
        
        elif temp_time_value > (time_value + soft_delay_limit):
            #Delay is more than soft timeout approved delay
            stamp_time(2, True, "soft timeout")
            time_value = temp_time_value
            stamp_time(2, False, "soft resume")
            
        
        #time is within time check delay limit
        else:
            #update time_value to current time
            time_value = temp_time_value
    
    #Somehow temp_time_value is less than time_value which should be handled by new day so something is wrong if this is entered
    else:
        print("Something went wrong!", time_value, "new", temp_time_value)

#Loop of regular checks if system is still active
def running(threadName = "Kim"):
    global sleep_time
    global debug_counter
    global working
    
    if(check_date()):
        check_time()
    #debug_counter += 1


def check_and_restore():
    if(fh.file_empty(recovery_file_name)):
        print("no valid restore file")
    else:
        restore_data = fh.read_data(recovery_file_name)
        fh.write_data_to_file(file_name, "a", restore_data)
        fh.delete_data_file(recovery_file_name)

def recovery_stamp_time():
    s = store_time_date(5, "Auto", True, get_work_time())
    fh.write_data_to_file(recovery_file_name, "w", s)

'''
def log_to_file(s):
    
    # Open a file
    global file_name
    
    #print("File!!", file_name, "content:", s)

    if os.stat(file_name).st_size == 0:
        fo.write(log_intro)
        fo.write("day\tdate\t\tid number\ttime\t\twork time\tE///\taction\tmessage\n")
    
    fo.write(s + "\n")
    fo.close()
    
    '''