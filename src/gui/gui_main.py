'''
Created on 23 nov. 2018

@author: ezasaju
'''

from tkinter import *
from tkinter import messagebox
from main import main_program



#import tkinter
#from tkinter import Button
#from tkinter.ttk import Frame

if __name__ == '__main__':
    pass


top = Tk()
top.minsize(width=250, height=100) 
#top.geometry("100x100")
frame = Frame(top)
frame.pack()

#main_program.initiate_parameters()


def quit():
    msg = messagebox.showinfo("Hi", "Hello World!")


def run_clocking():
    print ("start clocking")
    label.config(text = "Clocking")
    main_program.begin_clocking("user")
    
    
def stop_clocking():
    print ("end clocking")
    label.config(text = "Stopped")
    main_program.end_clocking("user")

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




'''
class Application(Frame):
    def msgBox(self):
    
    
    def say_hi(self):
        print("hello world!")
        
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit()
        
        self.QUIT.pack({"side": "left"})
        
        self.hi_there = Button(self)
        self.hi_there["text"]  = "Hello"
        self.hi_there["command"] = self.say_hi
        
        self.hi_there.pack({"side": "left"})
        
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
'''
