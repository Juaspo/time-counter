'''
Created on 14 jan. 2019

@author: ezasaju
'''
import os

filename = ".data"

def read_data(file_name):
    read_data = None
    try:
        with open(file_name) as f:
            read_data = f.read()
            print("data:", read_data)
        
        print("is file closed?", f.closed)
    except IOError:
        print("Could not read file")
    
    return read_data

def delete_data_file(file_name):
    try:
        os.remove(file_name)
        print("File Removed!")
    except IOError:
        print("Could not read file")


def write_data_to_file(file_name, mode, s):
    # Open a file
    
    #print("File!!", file_name, "content:", s)
    fo = open(file_name, mode)
    fo.write(s)
    fo.close()
    
def file_empty(file_name):
    try:
        if os.stat(file_name).st_size != 0:
            print("File exists but not empty:", file_name)
            return False
        else:
            print("File exist and is empty:", file_name)
            return True
        
    except IOError:
        print("Could not read file:", file_name)
        return True
    