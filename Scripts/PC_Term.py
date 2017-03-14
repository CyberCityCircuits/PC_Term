# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:24:54 2017

@author: admin
"""
import var, tasks


import os, sys
import datetime as dt
from pathlib import Path
#from bs4 import BeautifulSoup as bs
import lxml.etree as et

#from tkinter import *
from tkinter import Menu, Frame, BOTH, W
from tkinter import Tk, Label, messagebox



###DEFINE VARIBLES

#define system varibles
currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

x = 0


var.export_complete = 1

class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        tasks.delete_dir(var.dir_temp)
        tasks.mk_dir(var.dir_fresh)
        
        self.init_window()
        

    def init_window(self):
        self.master.title(var.long_app)
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
        #file_menu.add_command(label="Update", command=update)
        file_menu.add_command(label="Export Dataset", command=tasks.export_xml)
        #file_menu.add_command(label="List All Departments", command=tasks.list_dept)
        file_menu.add_command(label="Exit", command=tasks.client_exit)
        topbar.add_cascade(label="File", menu=file_menu)
        
        plu_menu.add_command(label="Survey PLUs", command=tasks.survey_plus)
        plu_menu.add_command(label="Remove Product Codes", command=tasks.run_pc_term)
        plu_menu.add_command(label="Remove Food Stamp Checks", command=tasks.remove_fs)
        plu_menu.add_command(label="Reset ID Checks by Department", command=reset_idchks)
        plu_menu.add_command(label="Set Food Stamp Checks by Department", command=set_fs)
        topbar.add_cascade(label="Edit PLUs", menu=plu_menu)
        
        help_menu.add_command(label="Directions", command=funct_not_supp)
        help_menu.add_command(label="About", command=show_about)
        topbar.add_cascade(label="Help", menu=help_menu)
        
        
def import_data():
    tasks.import_xml()
    show_dept()
    
    
def funct_not_supp():
    msg_error("Function Not Yet Supported")
    

def msg(text):
    messagebox.showinfo(var.long_app, text)
    
def msg_error(text):
    messagebox.showerror(var.long_app, text)

    
#command for reseting ID checks.    
def reset_idchks():
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T09: Check Error\nFile Not Found. \n ")   
    else:
        var.dept_alcohol_id = []
        var.dept_tobacco_id = []
        var.tobacco_id_count = 0
        var.alcohol_id_count = 0
        tasks.remove_idchecks()
        tasks.set_tobacco_ID()
        tasks.set_alcohol_ID()
        msg("All ID Checks Have Been Reset:"
            "\n\n" + str(var.tobacco_id_count) + " Tobacco ID Checks Have Been Added"
            "\n" + str(var.alcohol_id_count) + " Alcohol ID Checks Have Been Added")
            
#command for setting food stamps
def set_fs():
    var.dept_food_stamps = []
    var.fs_count = 0
    tasks.set_food_stamps()
    msg(str(var.fs_count) +  " Food Stamp Checks Have Been Added")        
        
#command for help > about
def show_about():
    msg(var.name + "\n"
        "Build: " + var.build_date + "\n\n"
        "By David Ray \n"
        "\n" + var.email + "\n\n"
        "www.DREAM-Enterprise.com")
    
    
#lists departments in the root window.
def show_dept():
    if not Path(var.dir_temp + "/poscfg.xml").is_file():
        msg_error("P01: Check Error\n'poscfg.xml' Not Found. \n ")   
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

        #msg("Processing Departments")
        
        for i, txt in enumerate(dept_list):
            l = Label(root, text=txt)
            row, col = divmod(i, 4)
            l.grid(row=row+1, column=col, sticky=W)
            
        var.dept_list = dept_list
             
                
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

