'''
Created on 18 dec. 2018

@author: ezasaju
'''
import os


def put_to_sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")