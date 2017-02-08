# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:14:01 2017

@author: admin
"""

import var, process, PC_Term, gui

import os, sys, re
import datetime as dt
from time import sleep
from shutil import copyfile
from shutil import rmtree as rm_dir
from pathlib import Path


#set varibles
export_complete = 1
        
#delete a directory
def delete_dir(dir_name):
    if os.path.exists(dir_name):
        rm_dir(dir_name)
    else:
        print ("Directory Doesn't Exist")
        
#delete file
def delete_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        print ("File Doesn't Exit")
        
#set date and time        
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

#copy files
def copy(fn1,fn2):
    if os.path.isfile(fn1):
        copyfile(fn1,fn2)
    else:
        print ("File Doesn't Exit")
       
def import_xml():
    global export_complete
    export_complete = 0
    mk_dir(var.dir_temp)
    
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
           #text = Label(Window, text=(file.ljust(35) + " Imported"))
           #text.pack()
           #pause(.03)
    gui.msg("Import Complete\nYour back up is in a folder\nnamed" + var.dir_dirty)
    #text.gui.pack()
    #pause(2)
    
def export_xml():
    global export_complete
    chk_file_temp(var.plu_xml)
        
    #set current date/time for directory name purposes
    set_date_time()

    #create var.dir_clean
    dir_put = (var.dir_clean + "-" + currdate + "-" + currtime)
    mk_dir(dir_put)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_temp):
       if file.endswith(".xml"):
           copy(var.dir_temp + "/" + file, dir_put + "/" + file)
               
    set_date_time()
    copy(var.dir_temp + "\\" + var.log_name + ".txt", dir_put + "\\" + var.log_name + ".txt")
           
    export_complete = 1
                      
    gui.msg("Export Complete\nYour export is in a folder\nnamed" + var.dir_clean)
    
    
    
    
#set wait command
def pause(value):
    if value == 0:   #if 0 is entered it creates a press any key prompt.
        os.system("pause")
    elif int(value):
        sleep(value)


#make directories as needed
def mk_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def mk_log():
    #creates and writes to log file
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","w")
    log_currdate = dt.date.today().strftime("%m/%d/%Y")
    log_currtime = dt.datetime.now().strftime("%H:%M:%S")
    f.write(var.long_app + " V" + var.version + "\n")
    f.write("Starting Date - " + log_currdate + "\n")
    f.write("Starting Time - " + log_currtime + "\n")
    f.write("\n")
    f.close()    


def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

#checks if file exists in var.dir_temp
def chk_file_temp(file_name):
    if not Path(var.dir_temp + "/" + file_name).is_file():
        gui.msg_error("Error: File Not Found. \n ")

        

#copy files
def copy(fn1,fn2):
    if os.path.isfile(fn1):
        copyfile(fn1,fn2)
    else:
        msg_error("Error: File Does Not Exist.")
        
#delete a directory
def delete_dir(dir_name):
    if os.path.exists(dir_name):
        rm_dir(dir_name)
    else:
        msg("Error: Directory Doesn't Exist")
        
#delete file
def delete_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        msg_error("Error: File Doe Not Exit")    