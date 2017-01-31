# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 13:23:32 2016

@author: David A Ray - CBE Inc.
"""

#import libraries
import os
import datetime as dt
import time
import shutil
import lxml.etree as et

#set console size and color
os.system('mode con: cols=50 lines=26')
os.system('color F')
os.system('cls')
os.system('echo off')

#set varibles
version = ('0.05.00')
dir_fresh = ('Put_PLUs_Here')
dir_clean = ('Cleaned_PLUs')
dir_dirty = ('Dirty_PLUs')
file_plu = ('PLUs.XML')
wait = 3
currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

#define commands
#splash screen
def logo():  
    print ("    -----------------------------------------")
    print ("             _______          ______ ")
    print ("            /       \        /      \.")
    print ("            $$$$$$$  |      /$$$$$$  |")
    print ("            $$ |__$$ |      $$ |  $$/")
    print ("            $$    $$/       $$ |")
    print ("            $$$$$$$/        $$ |   __")
    print ("            $$ |            $$ \__/  |")
    print ("            $$ |            $$    $$/")
    print ("            $$/              $$$$$$/")
    print ("     ________")   
    print ("    /        |")    
    print ("    $$$$$$$$/______    ______   _____  ____")
    print ("       $$ | /      \  /      \ /     \/    \ ")
    print ("       $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |")
    print ("       $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |")
    print ("       $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |")
    print ("       $$ |$$       |$$ |      $$ | $$ | $$ |")
    print ("       $$/  $$$$$$$/ $$/       $$/  $$/  $$/ ")
    print ("    -----------------------------------------")
    print ("        Product Code Terminator V " + version)    
    print ("                   David A Ray")
    print ("")
    print ("     The existing PLU file is being backed up")
    print ("         to a folder called \"Dirty PLUs\".")

#copy plu file to working directory
def copy_plu():
    shutil.copyfile(dir_fresh + "/" + file_plu, file_plu)

#back up plu file to backup directory
def backup_plu():
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    os.makedirs(dir_bu)
    shutil.copyfile(file_plu, dir_bu + "/" + file_plu)

#process plu file
def process():
    tree = et.parse(file_plu)
    root = tree.getroot()
    for pcode in root.iter('pcode'):
        pcode.text = str(0)
    tree.write(file_plu,encoding="UTF-8",xml_declaration=True)

#copy processed plu file to clean directory
def put_plu():
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    os.makedirs(dir_put)    
    shutil.copyfile(file_plu, dir_put + "/" + file_plu)

#delete plu file from working directory
def delete_plu():
    os.remove(file_plu)    

#run commands
if __name__ == "__main__":
    logo()
    time.sleep(wait)
    copy_plu()
    backup_plu()
    process()
    put_plu()
    delete_plu()
