# -*- coding: utf-8 -*-
"""
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
application = "PC_Term"
long_app = "Product Code Terminator"
version = "0.05.11"
email = "David@DREAM-Enterprise.com"
dir_fresh = "Put_PLUs_Here"
dir_clean = "Clean_PLUs"
dir_dirty = "Dirty_PLUs"
file_xml = "PLUs.xml"
log_name = "PC_Term Report"
tag = "pcode"
value = 0
count_tag = "<domain:PLU>"
count_low = 250

x = 0

count_plu = 0
tag_plu = "<domain:PLU>"

#define system varibles
wait = 3.0
width = 50
lines = 31
cent_width = int(width)-1

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
    print ()
    print ("-----------------------------------------".center(cent_width))
    print ("         _______          ______         ".center(cent_width))
    print ("        /       \        /      \.       ".center(cent_width))
    print ("        $$$$$$$  |      /$$$$$$  |       ".center(cent_width))
    print ("        $$ |__$$ |      $$ |  $$/        ".center(cent_width))
    print ("        $$    $$/       $$ |             ".center(cent_width))
    print ("        $$$$$$$/        $$ |   __        ".center(cent_width))
    print ("        $$ |            $$ \__/  |       ".center(cent_width))
    print ("        $$ |            $$    $$/        ".center(cent_width))
    print ("        $$/              $$$$$$/         ".center(cent_width))
    print (" ________                                ".center(cent_width))
    print ("/        |                               ".center(cent_width))
    print ("$$$$$$$$/______    ______   _____  ___   ".center(cent_width))
    print ("   $$ | /      \  /      \ /     \/    \ ".center(cent_width))
    print ("   $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |".center(cent_width))
    print ("   $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |".center(cent_width))
    print ("   $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |".center(cent_width))
    print ("   $$ |$$       |$$ |      $$ | $$ | $$ |".center(cent_width))
    print ("   $$/  $$$$$$$/ $$/       $$/  $$/  $$/ ".center(cent_width))
    print ("-----------------------------------------".center(cent_width))
    print (("Product Code Terminator V " + version).center(cent_width))
    print ("David A Ray".center(cent_width))
    print ()
    print (("Contact: " + email).center(cent_width))
    print ()
    print ("The existing PLU file is being backed up in".center(cent_width))
    print (("a folder called \"" + dir_dirty + "\".").center(cent_width))
    print ()
    print ("The corrected PLU file is being put in".center(cent_width))
    print (("a folder valled \"" + dir_clean + "\".").center(cent_width))

#make dir_fresh if needed
def mk_dir_fresh():
    if not os.path.exists(dir_fresh):
        os.makedirs(dir_fresh)
        
#check if file_xml exists
def chk_file_fresh():
    file_fresh = Path(dir_fresh + "\\" + file_xml)
    if not file_fresh.is_file():
        os.system("cls")
        print ()
        print ()
        print (("Product Code Terminator V " + version).center(cent_width))
        print ()
        print ()
        print ("FILE NOT FOUND".center(cent_width))
        print ()
        print (("Please move your " + file_xml + " file to").center(cent_width))
        print (("the directory named " + dir_fresh).center(cent_width))
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
        print ()
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
    global x
    tree = et.parse(file_xml)
    root = tree.getroot()
    for xml_tag in root.iter(tag):
        xml_tag.text = str(value)
    tree.write(file_xml,encoding="UTF-8",xml_declaration=True)
    
    for c in root:
        print (root[x][0].text, root[x][3].text, root[x][2].text)
        x += 1
        #sleep(.00001)

#copy processed plu file to clean directory
def put_plu():
    global dir_put
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    os.makedirs(dir_put)    
    copy(file_xml, dir_put + "/" + file_xml)

#delete plu file from working directory
def delete_plu():
    os.remove(file_xml)

#count how many plus there are
def import_data():
    global str_data
    with open (file_xml, "r") as raw_data:
        str_data = raw_data.readlines()        
                
def count_str():
    global count_occ
    count_occ = len(re.findall(count_tag, str(str_data)))
    
def complete():
    os.system("cls")
    print ()
    print ()
    print ()
    print ("Process is Complete.".center(cent_width))
    print ()
    print (("There are " + str(count_occ) + " PLUs.").center(cent_width))
    print ()
    if count_occ <= count_low:
        print ("WARNING - WARNING - WARNING - WARNING - WARNING".center(cent_width))
        print ()
        print ("Your PLU count is lower than anticipated.".center(cent_width))
        print ("Please confirm that this number is accurate.".center(cent_width))
        print ()
        print ("This error can be caused by using the wrong".center(cent_width))
        print ("version of SMS Import/Export.  Use the".center(cent_width))
        print (" Sapphire's SMS Configuration Manager to".center(cent_width))
        print ("ensure you have all of the PLUs.".center(cent_width))
        print ()
        print ("WARNING - WARNING - WARNING - WARNING - WARNING".center(cent_width))
    else:
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
    
def log_file():
    f = open(dir_put + "\\" + log_name + ".txt","w")
    log_currdate = dt.date.today().strftime("%m/%d/%Y")
    log_currtime = dt.datetime.now().strftime("%H:%M:%S")
    f.write(long_app + " V" + version + "\n")
    f.write("Starting Date - " + log_currdate + "\n")
    f.write("Starting Time - " + log_currtime + "\n")
    f.write("\n")
    f.write("There were " + str(count_occ) + " PLUs in the file provided.")
    if count_occ <= count_low:
        f.write("\n")
        f.write("\n")
        f.write ("WARNING - WARNING - WARNING - WARNING - WARNING\n")
        f.write("\n")
        f.write ("Your PLU count is lower than anticipated.  Please confirm that this number is accurate.\n")
        f.write("\n")
        f.write ("This error can be caused by using the wrong version of SMS Import/Export.  Use the Sapphire's SMS Configuration Manager to ensure you have all of the PLUs.\n")
        f.write("\n")
        f.write ("WARNING - WARNING - WARNING - WARNING - WARNING\n")
    f.flush()
    
def main():
    mk_dir_fresh()
    logo()
    sleep(wait)
    chk_file_fresh()
    copy_plu()
    backup_plu() 
    import_data()
    count_str()
    process()  
    put_plu()
    delete_plu()
    log_file()
    complete()
 
#run commands
if __name__ == "__main__":
    main()