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
        
        file_menu.add_command(label="Import Dataset", command=tasks.import_xml)
        file_menu.add_command(label="Export Dataset", command=tasks.export_xml)
        file_menu.add_command(label="List All Departments", command=tasks.list_dept)
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
        
def msg(text):
    messagebox.showinfo(app_name, text)
    
def msg_error(text):
    messagebox.showerror(app_name, text)
   
def show_about():
    msg(long_app + " V" + version + "\nBuild: " + build_date + "\n\nBy David Ray \nwww.DREAM-Enterprise.com")
    
root = Tk()
root.geometry("400x600")







if not Path(var.dir_fresh + "/" + var.plu_xml).is_file():
    msg_error("T05: Import Error\nFile Not Found.\n\nPlease Place Your Dataset\nIn The Folder Named\n" + var.dir_fresh)   

else:
    tasks.mk_dir(var.dir_temp)
    tasks.mk_log()
    
    #set current date/time for directory name purposes
    tasks.set_date_time()

    #create backup directory
    dir_bu = (var.dir_dirty + "-" + tasks.currdate + "-" + tasks.currtime)
    tasks.mk_dir(dir_bu)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_fresh):
       if file.endswith(".xml"):
           tasks.copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
           tasks.copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
           #text = Label(Window, text=(file.ljust(35) + " Imported"))
           #text.pack()
           #pause(.03)
    msg("Import Complete\n\nYour Back Up Is In a Folder\nNamed " + var.dir_dirty)

    if not Path(var.dir_temp + "/poscfg.xml").is_file():
        msg_error("T07: Check Error\n'poscfg.xml' Not Found. \n ")   
    else:
    
        #x = 0
        dept_list = []
        
        
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root_xml = tree.getroot()
        
        for dept in root_xml.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            name = (attributes["name"])
            
            #print ((sysid.rjust(4)) + " - " + name.ljust(20))
            #sleep(.02)
            #x += 1
            #if x == (lines-7) or x == ((lines-7)*2) or x == ((lines-7)*3):
            dept = (sysid.rjust(4) + " " + name.ljust(20))
            dept_list.append(dept)

        msg("Processing Departments")


    row = 1
    for i, txt in enumerate(dept_list):
        l = Label(root, text=txt)
        col = 0 if i%2 == 0 else 1
        l.grid(row=row, column=col)
        if col == 1:
            row += 1

'''
#global export_complete
export_complete = 0

if not Path(var.dir_fresh + "/" + var.plu_xml).is_file():
    msg_error("T05: Import Error\nFile Not Found.\n\nPlease Place Your Dataset\nIn The Folder Named\n" + var.dir_fresh)   

else:
    tasks.mk_dir(var.dir_temp)
    tasks.mk_log()
    
    #set current date/time for directory name purposes
    tasks.set_date_time()

    #create backup directory
    dir_bu = (var.dir_dirty + "-" + tasks.currdate + "-" + tasks.currtime)
    tasks.mk_dir(dir_bu)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_fresh):
       if file.endswith(".xml"):
           tasks.copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
           tasks.copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
           #text = Label(Window, text=(file.ljust(35) + " Imported"))
           #text.pack()
           #pause(.03)
    msg("Import Complete\n\nYour Back Up Is In a Folder\nNamed " + var.dir_dirty)


#file_temp_merch = Path(dir_temp + "\\" + "poscfg.xml")
if not Path(var.dir_temp + "/poscfg.xml").is_file():
    msg_error("T07: Check Error\n'poscfg.xml' Not Found. \n ")   
else:

    #x = 0
    dept_list = []
    
    
    tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        name = (attributes["name"])
        
        #print ((sysid.rjust(4)) + " - " + name.ljust(20))
        #sleep(.02)
        #x += 1
        #if x == (lines-7) or x == ((lines-7)*2) or x == ((lines-7)*3):
        dept = (sysid.rjust(4) + " " + name.ljust(20))
        dept_list.append(dept)
        #dept_list.append(name)
    
    #dept_list.insert(0, "List of Departments")
    #dept_list_temp = dept_list
    dept_list_len = len(dept_list)
    #iterable = range(len(dept_list))
    
    
    #dept_list_final = dept_list_temp
    
    #x=0
    #for item in iterable:
    #   x += 1
    #   if (x % 2 == 0): #even
    #       add_item = (dept_list.pop(0) + "    " + dept_list.pop(0))
    #       dept_list_final.append(add_item)       
    #dept_list = '\n'.join(dept_list_final)
    #dept_list[0].grid(row=0, column=0)
    #dept_list[1].grid(row=0, column=1)
    #dept_list[2].grid(row=1, column=0)
    #dept_list[3].grid(row=1, column=1)

    x = dept_list_len
    if not (x % 2 == 0):#odd
        x+=1
    
    r = x / 2
        
for rows in range(4):
    for columns in range(2):
        Label(root, text=(dept_list.pop(0))(rows,columns),
            borderwidth=1 ).grid(row=rows,column=columns)
'''

app = Window(root)    

root.mainloop()

