# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:24:54 2017

@author: admin
"""
import tasks, PC_Term, process, var


import os
import datetime as dt
from shutil import copyfile

from tkinter import *
from tkinter import Menu, Frame, BOTH
from tkinter import Tk, Label, messagebox



###DEFINE VARIBLES
app_name = var.app_name
long_app = app_name
version = var.version





#define system varibles
currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

x = 0



export_complete = 1

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title(app_name)
        self.pack(fill=BOTH, expand=1)
        
        #exit_button = Button(self, text = "Exit", command=exit)
        #exit_button.place(x = 170, y = 270)
        
        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        
        file_menu = Menu(topbar)
        #edit_menu = Menu(topbar)
        remove_menu = Menu(topbar)
        add_menu = Menu(topbar)
        help_menu = Menu(topbar)
        
        file_menu.add_command(label="Import Dataset", command=import_xml)
        file_menu.add_command(label="Export Dataset")
        file_menu.add_command(label="List All Departments")
        file_menu.add_command(label="Exit", command=self.client_exit)
        topbar.add_cascade(label="File", menu=file_menu)
        
        
        #edit.add_command(label="Remove Product Codes")
        #edit.add_command(label="Remove ID Checks")
        #edit.add_command(label="Remove Food Stamp Checks")
        #edit.add_command(label="Set ID Checks by Department")
        #edit.add_command(label="Set Food Stamp Checks by Department")
        #topbar.add_cascade(label="Edit", menu=edit_menu)
        

        remove_menu.add_command(label="Remove Product Codes") #command=PC_Term.run_pc_term)
        remove_menu.add_command(label="Remove ID Checks")
        remove_menu.add_command(label="Remove Food Stamp Checks")

        topbar.add_cascade(label="Remove", menu=remove_menu)

        add_menu.add_command(label="Set ID Checks by Department")
        add_menu.add_command(label="Set Food Stamp Checks by Department")


        
    
        topbar.add_cascade(label="Add", menu=add_menu)
        
        
        
        
        topbar.add_cascade(label="Help", menu=help_menu)
        
        
        
        
        
        
    def client_exit(self):
        exit()
        
#copy files
def copy(fn1,fn2):
    if os.path.isfile(fn1):
        copyfile(fn1,fn2)
    else:
        print ("File Doesn't Exit")
        
def msg(text):
    messagebox.showinfo(app_name, text)
    
def import_xml():
    global export_complete
    export_complete = 0
    mk_dir("TEMP")
    
    mk_log()
   
    #set current date/time for directory name purposes
    set_date_time()

    #create backup directory
    dir_bu = (var.dir_dirty + "-" + currdate + "-" + currtime)
    mk_dir(dir_bu)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_fresh):
       if file.endswith(".xml"):
           copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
           copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
           text = Label(Window, text=(file.ljust(35) + " Imported"))
           text.pack()
           tasks.pause(.03)
           
    
    text = Label(Window, text="IMPORT COMPLETE")
    text.gui.pack()
    tasks.pause(2)
    
    

#make directories as needed
def mk_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def mk_log():
    #creates and writes to log file
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","w")
    log_currdate = dt.date.today().strftime("%m/%d/%Y")
    log_currtime = dt.datetime.now().strftime("%H:%M:%S")
    f.write(long_app + " V" + version + "\n")
    f.write("Starting Date - " + log_currdate + "\n")
    f.write("Starting Time - " + log_currtime + "\n")
    f.write("\n")
    f.close()    


def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

    
    
root = Tk()
root.geometry("400x300")

app = Window(root)    

root.mainloop()

