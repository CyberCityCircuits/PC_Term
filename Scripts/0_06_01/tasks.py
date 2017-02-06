# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:14:01 2017

@author: admin
"""

import var, process, PC_Term

import os, sys, re
import datetime as dt
from time import sleep
from shutil import copyfile
from shutil import rmtree as rm_dir
from pathlib import Path


#set wait command
def pause(value):
    if value == 0:   #if 0 is entered it creates a press any key prompt.
        os.system("pause")
    elif int(value):
        sleep(value)
        
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
        
#checks if file exists in var.dir_temp
def chk_file_temp(file_name):
    if not Path(var.dir_temp + "/" + file_name).is_file():
        PC_Term.header()
        print ()
        print ("FILE NOT FOUND".center(var.cent_width))
        print ()
        print (("Please move your store backup XMLs to").center(var.cent_width))
        print (("the directory named " + var.dir_fresh + " and then").center(var.cent_width))
        print (("use the option to IMPORT YOUR BACKUP.").center(var.cent_width))
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        print ()
        os.system("pause")
        PC_Term.main_menu()        
