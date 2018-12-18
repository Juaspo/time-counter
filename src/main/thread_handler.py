'''
Created on 11 dec. 2018

@author: ezasaju
'''
'''
import threading
from main import main_program

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()
        
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
    
    def run(self):
        print("Thread running!")
        main_program.running("Kimpa")
        
'''

