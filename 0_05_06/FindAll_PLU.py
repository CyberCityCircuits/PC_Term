# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 13:23:32 2016

@author: David A Ray
"""

#import libraries
import os
from sys import exit
import datetime as dt
from time import sleep
from shutil import copyfile as copy
import lxml.etree as et
from pathlib import Path
import re

#set varibles
version = ("0.05.04")
dir_fresh = ("Put_PLUs_Here")
dir_clean = ("Clean_PLUs")
dir_dirty = ("Dirty_PLUs")
file_xml = ("PLUs.xml")
tag = ("pcode")
value = 0

count = 0
tag_count = ("<domain:PLU>")

#define system varibles
wait = 3.0
width = 50
lines = 30
cent_width = (int(width)-1)

currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

#set console size and color
os.system("mode con: cols=" + str(width) + " lines=" + str(lines))
os.system("color F")
os.system("cls")
os.system("echo off")

#define commands
#splash screen
def logo():  
    print ("")
    print ("-----------------------------------------").center(cent_width)
    print ("         _______          ______         ").center(cent_width)
    print ("        /       \        /      \.       ").center(cent_width)
    print ("        $$$$$$$  |      /$$$$$$  |       ").center(cent_width)
    print ("        $$ |__$$ |      $$ |  $$/        ").center(cent_width)
    print ("        $$    $$/       $$ |             ").center(cent_width)
    print ("        $$$$$$$/        $$ |   __        ").center(cent_width)
    print ("        $$ |            $$ \__/  |       ").center(cent_width)
    print ("        $$ |            $$    $$/        ").center(cent_width)
    print ("        $$/              $$$$$$/         ").center(cent_width)
    print (" ________                                ").center(cent_width)
    print ("/        |                               ").center(cent_width)
    print ("$$$$$$$$/______    ______   _____  ___  _").center(cent_width)
    print ("   $$ | /      \  /      \ /     \/    \ ").center(cent_width)
    print ("   $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |").center(cent_width)
    print ("   $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |").center(cent_width)
    print ("   $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |").center(cent_width)
    print ("   $$ |$$       |$$ |      $$ | $$ | $$ |").center(cent_width)
    print ("   $$/  $$$$$$$/ $$/       $$/  $$/  $$/ ").center(cent_width)
    print ("-----------------------------------------").center(cent_width)
    print ("Product Code Terminator V " + version).center(cent_width)
    print ("David A Ray").center(cent_width)
    print ("")
    print ("The existing PLU file is being backed up in").center(cent_width)
    print ("a folder called \"" + dir_dirty + "\".").center(cent_width)
    print ("")
    print ("The corrected PLU file is being put in").center(cent_width)
    print ("a folder valled \"" + dir_clean + "\".").center(cent_width)

#make dir_fresh if needed
def mk_dir_fresh():
    if not os.path.exists(dir_fresh):
        os.makedirs(dir_fresh)
        
#check if file_xml exists
def chk_file_fresh():
    file_fresh = Path(dir_fresh + "\\" + file_xml)
    if not file_fresh.is_file():
        os.system("cls")
        print ("")
        print ("")
        print ("Product Code Terminator V " + version).center(cent_width)
        print ("")
        print ("")
        print ("FILE NOT FOUND").center(cent_width)
        print ("")
        print ("Please move your " + file_xml + " file to").center(cent_width)
        print ("the directory named " + dir_fresh).center(cent_width)
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        print ("")
        os.system("pause")
        exit()

#copy plu file to working directory
def copy_plu():
    copy(dir_fresh + "/" + file_xml, file_xml)

#back up plu file to backup directory
def backup_plu():
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    os.makedirs(dir_bu)
    copy(file_xml, dir_bu + "/" + file_xml)

#process plu file
def process():
    tree = et.parse(file_xml)
    root = tree.getroot()
    for xml_tag in root.iter(tag):
        xml_tag.text = str(value)
    tree.write(file_xml,encoding="UTF-8",xml_declaration=True)

#copy processed plu file to clean directory
def put_plu():
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    os.makedirs(dir_put)    
    copy(file_xml, dir_put + "/" + file_xml)

def count_plu(file):
    

#delete plu file from working directory
def delete_plu():
    os.remove(file_xml)
    
#run commands
if __name__ == "__main__":
    #mk_dir_fresh()
    #logo()
    #sleep(wait)
    chk_file_fresh()
    copy_plu()
    count_plu(file_plu)
    #backup_plu() 
    #process()  
    #put_plu()
    #delete_plu()
