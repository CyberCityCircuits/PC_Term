# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:24:54 2017

@author: admin
"""
import var, tasks


import os, sys
import datetime as dt
from pathlib import Path
from bs4 import BeautifulSoup as bs
import lxml.etree as et

from tkinter import *
from tkinter import Menu, Frame, BOTH, W
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
        tasks.delete_dir(var.dir_temp)
        tasks.mk_dir(var.dir_fresh)
        
        self.init_window()
        

    def init_window(self):
        self.master.title(long_app)
        #self.pack(fill=BOTH, expand=1)
        
        #exit_button = Button(self, text = "Exit", command=exit)
        #exit_button.place(x = 170, y = 270)
        
        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        
        file_menu = Menu(topbar)
        #edit_menu = Menu(topbar)
        #remove_menu = Menu(topbar)
        #add_menu = Menu(topbar)
        plu_menu = Menu(topbar)
        help_menu = Menu(topbar)
        
        file_menu.add_command(label="Import Dataset", command=import_data)
        file_menu.add_command(label="Export Dataset", command=tasks.export_xml)
        #file_menu.add_command(label="List All Departments", command=tasks.list_dept)
        file_menu.add_command(label="Exit", command=client_exit)
        topbar.add_cascade(label="File", menu=file_menu)
        
        plu_menu.add_command(label="Remove Product Codes", command=tasks.run_pc_term)
        plu_menu.add_command(label="Remove Food Stamp Checks", command=tasks.remove_fs)
        plu_menu.add_command(label="Reset ID Checks by Department")
        plu_menu.add_command(label="Set Food Stamp Checks by Department")
        topbar.add_cascade(label="Edit PLUs", menu=plu_menu)
        
        help_menu.add_command(label="Directions")
        help_menu.add_command(label="About", command=show_about)
        topbar.add_cascade(label="Help", menu=help_menu)
        
        
        
        
        
def client_exit():
    sys.exit() 
    
def import_data():
    tasks.import_xml()
    show_dept()
    
def show_dept():
    if not Path(var.dir_temp + "/poscfg.xml").is_file():
        msg_error("T07: Check Error\n'poscfg.xml' Not Found. \n ")   
    else:
    
        dept_list = []
        
        
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root_xml = tree.getroot()
        
        for dept in root_xml.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            name = (attributes["name"])
            
            dept_list.append(sysid)
            dept_list.append(name)

        msg("Processing Departments")

        
        for i, txt in enumerate(dept_list):
            l = Label(root, text=txt)
            row, col = divmod(i, 4)
            l.grid(row=row+1, column=col, sticky=W)
        
def msg(text):
    messagebox.showinfo(app_name, text)
    
def msg_error(text):
    messagebox.showerror(app_name, text)
   
def show_about():
    msg(long_app + " V" + version + "\nBuild: " + build_date + "\n\nBy David Ray \nwww.DREAM-Enterprise.com")

    '''
def import_xml():
    
    if not Path(var.dir_fresh + "/" + var.plu_xml).is_file():
        msg_error("T05: Import Error\nFile Not Found.\n\nPlease Place Your Dataset\nIn The Folder Named\n" + var.dir_fresh)   
    
    else:
        tasks.mk_dir(var.dir_temp)
        tasks.mk_log()
        
        tasks.set_date_time()
    
        dir_bu = (var.dir_dirty + "-" + tasks.currdate + "-" + tasks.currtime)
        tasks.mk_dir(dir_bu)
        
        for file in os.listdir(var.dir_fresh):
           if file.endswith(".xml"):
               tasks.copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
               tasks.copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
        msg("Import Complete\n\nYour Back Up Is In a Folder\nNamed " + var.dir_dirty)
    
        if not Path(var.dir_temp + "/poscfg.xml").is_file():
            msg_error("T07: Check Error\n'poscfg.xml' Not Found. \n ")   
        else:
        
            dept_list = []
            
            
            tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
            root_xml = tree.getroot()
            
            for dept in root_xml.iter('department'):
                attributes = (dept.attrib)
                sysid = (attributes["sysid"])
                name = (attributes["name"])
                
                dept_list.append(sysid)
                dept_list.append(name)
    
            msg("Processing Departments")
    
            
            for i, txt in enumerate(dept_list):
                l = Label(root, text=txt)
                row, col = divmod(i, 4)
                l.grid(row=row+1, column=col)

                '''
                
root = Tk()

w = 300 # width for the Tk root
h = 600 #height for the Tk root

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/4) - (w/2)
y = (hs/2.5) - (h/2)

# set the dimensions of the screen 
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

                
app = Window(root)    

import_data()

root.mainloop()

