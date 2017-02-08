# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:24:54 2017

@author: admin
"""
import var, tasks, process, PC_Term


import os, sys
import datetime as dt
from time import sleep
from shutil import copyfile
from shutil import rmtree as rm_dir
from pathlib import Path


from tkinter import *
from tkinter import Menu, Frame, BOTH
from tkinter import Tk, Label, messagebox



###DEFINE VARIBLES
app_name = var.app_name
long_app = var.long_app
version = var.version
build_date = var.build_date




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
        self.master.title(long_app)
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
        
        file_menu.add_command(label="Import Dataset", command=tasks.import_xml)
        file_menu.add_command(label="Export Dataset")
        file_menu.add_command(label="List All Departments")
        file_menu.add_command(label="Exit", command=client_exit)
        topbar.add_cascade(label="File", menu=file_menu)
        
        remove_menu.add_command(label="Remove Product Codes") #command=PC_Term.run_pc_term)
        remove_menu.add_command(label="Remove ID Checks")
        remove_menu.add_command(label="Remove Food Stamp Checks")
        topbar.add_cascade(label="Remove", menu=remove_menu)

        add_menu.add_command(label="Set ID Checks by Department")
        add_menu.add_command(label="Set Food Stamp Checks by Department")
        topbar.add_cascade(label="Add", menu=add_menu)
        
        
        
        help_menu.add_command(label="Directions")
        help_menu.add_command(label="About", command=show_about)
        topbar.add_cascade(label="Help", menu=help_menu)
        
        
        
        
        
        
        
        
def msg(text):
    messagebox.showinfo(app_name, text)
    
def msg_error(text):
    messagebox.showerror(app_name, text)


def client_exit():
    sys.exit() 

    
def show_about():
    msg(long_app + " V" + version + "\nBuild: " + build_date + "\n\nBy David Ray \nwww.DREAM-Enterprise.com")
    
def import_xml():
    tasks.import_xml()
    
root = Tk()
root.geometry("400x300")

app = Window(root)    

root.mainloop()

