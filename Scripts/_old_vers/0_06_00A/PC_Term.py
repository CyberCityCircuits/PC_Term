# -*- coding: utf-8 -*-
"""
@author: David A Ray
"""

#import libraries
import os
import sys
import datetime as dt
from time import sleep
from shutil import copyfile as copy
from shutil import rmtree as rm_dir
import lxml.etree as et
from pathlib import Path
import re

#set varibles
application = "PC_Term"
long_app = "Product Code Terminator"
version = "0.06.00A"
email = "David@DREAM-Enterprise.com"
name = long_app + "  V" + version
dir_fresh = "Put_XMLs_Here"
dir_clean = "Processed_XMLs"
dir_dirty = "BackUp_XMLs"
dir_temp = "TEMP"
plu_xml = "PLUs.xml"
log_name = "PC_Term Report"
tag = "pcode"
value = 0
count_tag = "<domain:PLU>"
count_low = 250
count_plu = 0
tag_plu = "<domain:PLU>"
var_not_found = 0

#define system varibles
wait = 3.0
width = 50
lines = 31
cent_width = int(width)-1

currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

x = 0

#set console size and color
os.system("mode con: cols=" + str(width) + " lines=" + str(lines))
os.system("color F")
os.system("cls")
os.system("echo off")

#define menu titles
menu_00 = "0 - Exit"
menu_01 = "1 - Remove Product Codes from PLU file"
menu_02 = "2 - Function Not Supported"
menu_03 = "3 - Function Not Supported" 
menu_04 = "4 - Function Not Supported"
menu_05 = "5 - Function Not Supported"
menu_06 = "6 - Function Not Supported"
menu_07 = "7 - Function Not Supported"
menu_08 = "8 - Function Not Supported"
menu_09 = "9 - Check Store Backup"

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
    print ((name).center(cent_width))
    print ("David A Ray".center(cent_width))
    print ()
    print (("Contact: " + email).center(cent_width))
    print ()
    print ("The existing XML files are being backed up in".center(cent_width))
    print (("a folder called \"" + dir_dirty + "\".").center(cent_width))
    print ()
    print ("The corrected XML files are being put in".center(cent_width))
    print (("a folder valled \"" + dir_clean + "\".").center(cent_width))

#Headers
def header():
    os.system("cls")
    print ()
    print ((name).center(cent_width))
    print ("David A Ray".center(cent_width))
    print ()
    
    
#main menu
def main_menu():
    header()
    print ()
    print ()
    print ("  " + menu_00)
    print ("  " + menu_01)
    print ("  " + menu_02)
    print ("  " + menu_03)
    print ("  " + menu_04)
    print ("  " + menu_05)
    print ("  " + menu_06)
    print ("  " + menu_07)
    print ("  " + menu_08)
    print ("  " + menu_09)
    
    option = input("  Enter Your Selection: ")
    if option == ("0"):
        end()
    elif option == ("1"):
        run_pc_term()
    elif option == ("2"):
        funct_not_supp()
    elif option == ("3"):
        funct_not_supp()
    elif option == ("4"):
        funct_not_supp()
    elif option == ("5"):
        funct_not_supp()
    elif option == ("6"):
        funct_not_supp()
    elif option == ("7"):
        funct_not_supp()
    elif option == ("8"):
        funct_not_supp()
    elif option == ("9"):
        chk_store_backup()
        
def funct_not_supp():
    header()
    print ()
    print ("FUNCTION NOT SUPPORTED".center(cent_width))
    print ()
    print ()
    print ()
    sleep(wait)
    main_menu()
   
#make directories as needed
def mk_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

'''
#make dir_fresh if needed
def mk_dir_fresh():
    if not os.path.exists(dir_fresh):
        os.makedirs(dir_fresh)
        
#make dir_temp if needed
def mk_dir_temp():
    if not os.path.exists(dir_temp):
        os.makedirs(dir_temp)
'''
       
#checks if files exist in dir_fresh by attribute        
def chk_file_fresh(title, file_name):
    global var_not_found
    if not os.path.isfile(dir_fresh + "//" + file_name):
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Not Found"))
        var_not_found = 1
    else:
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Exists"))
       

        
def chk_store_backup():
    global var_not_found
    var_not_found = 0
    header()
    chk_file_fresh("Merchandise", "poscfg.xml")
    chk_file_fresh("PLUs", "PLUs.xml")
    chk_file_fresh("Sales Config", "salescfg.xml")
    print()
    print()
    if var_not_found == 1:
        print (("If any files are not found.").center(cent_width))
        print (("Please move your store backup XMLs to").center(cent_width))
        print (("the directory named " + dir_fresh).center(cent_width))

    print()
    os.system("pause")
    main_menu()

#process plu file
def remove_pcode():
    global x
    x=0
    tree = et.parse(dir_temp + "/" + plu_xml)
    root = tree.getroot()
    for xml_tag in root.iter(tag):
        xml_tag.text = str(value)
    tree.write(dir_temp + "/" + plu_xml,encoding="UTF-8",xml_declaration=True)
    
    for c in root:
        print (root[x][0].text, root[x][3].text, root[x][2].text)
        x += 1
        #sleep(.00001)

#delete plu file from working directory
def delete_xml(xml_name):
    os.remove(xml_name)
    
#delete a directory
def delete_dir(dir_name):
    rm_dir(dir_name)

    

def run_pc_term():
    #global str_data
    #global count_occ
    #global dir_put

    #set current date/time for directory name purposes
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

    #check is PLU fole is in dir_fresh
    file_fresh_plu = Path(dir_fresh + "\\" + plu_xml)
    if not file_fresh_plu.is_file():
        header()
        print ()
        print ("FILE NOT FOUND".center(cent_width))
        print ()
        #print (("Please move your " + plu_xml + " file to").center(cent_width))
        print (("Please move your store backup XMLs to").center(cent_width))
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
        main_menu()

    mk_dir(dir_temp)
    #copy PLUs to TEMP folder
    copy(dir_fresh + "/" + plu_xml, dir_temp + "/" + plu_xml)
    #make backup folder and copy to backup
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    mk_dir(dir_bu)
    copy(dir_temp + "/" + plu_xml, dir_bu + "/" + plu_xml)
    #import data
    with open (dir_temp + "/" + plu_xml, "r") as raw_data:
        str_data = raw_data.readlines()        
    #count PLUs
    count_occ = len(re.findall(count_tag, str(str_data)))
    
    remove_pcode()  

    #creates and copys processed PLU file to a processed folder
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    mk_dir(dir_put)
    copy(dir_temp + "/" + plu_xml, dir_put + "/" + plu_xml)
    
    delete_xml(dir_temp + "/" + plu_xml)
    delete_dir(dir_temp)
    
    #creates and writes to log file
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
    
    #prints on the console completion information.
    header()
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
    main_menu()

def end():
    header()
    print ()
    print ("...Program Ending...".center(cent_width))
    print ()
    print ()
    print ()
    sleep(1)
    sys.exit()    
    
#run commands
if __name__ == "__main__":
    mk_dir(dir_fresh)
    logo()
    sleep(wait)
    
    main_menu()
