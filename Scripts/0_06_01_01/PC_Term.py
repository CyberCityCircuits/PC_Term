# -*- coding: utf-8 -*-
"""
@author: David A Ray
"""

#import libraries
import os
import sys
import datetime as dt
from shutil import copyfile as copy
from shutil import rmtree as rm_dir
import lxml.etree as et
from bs4 import BeautifulSoup as bs
import re

import tasks, var, process, gui

#set varibles
application = "PC_Term"
long_app = "Product Code Terminator"
version = "0.06.01"
email = "David@DREAM-Enterprise.com"
name = long_app + "  V" + version

cent_width = var.cent_width


plu_count_low = 250
count_plu = 0
tag_plu = "<domain:PLU>"
var_not_found = 0
export_complete = 1
dept_tobacco_id = []
dept_alcohol_id = []
dept_food_stamps = []
full_dept_list = []

#define system varibles
currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

x = 0

#set console size and color
#os.system("mode con: cols=" + str(var.width) + " lines=" + str(var.lines))
#os.system("color F")
#os.system("cls")
#os.system("echo off")


#define commands
       
#checks if files exist in var.dir_fresh by attribute        
def chk_file_fresh(title, file_name):
    global var_not_found
    if not os.path.isfile(var.dir_fresh + "//" + file_name):
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Not Found"))
        var_not_found = 1
    else:
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Exists"))
        
        
#check to see if files are present in var.dir_fresh
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
        text = gui.Label(gui.Window,text = "If any files are not found. \n Please move your store backup XMLs to \n the directory named " + var.dir_fresh)
        text.gui.pack()
        
    print()
    tasks.pause(0)
    
        
#delete a directory
def delete_dir(dir_name):
    if os.path.exists(dir_name):
        rm_dir(dir_name)
        
#delete plu file from working directory
def delete_xml(xml_name):
    if os.path.isfile(xml_name):
        os.remove(xml_name)

def end():
    global export_complete
    header()
    if export_complete == 0:
        print ()
        print ("You XML files were never saved after changes.".center(cent_width))
        print ("Are you sure you would like to exit?  No changes".center(cent_width))
        print ("will be saved.".center(cent_width))
        print ()
        option = input("Would you like to discard your changes? (Y/N)".rjust(cent_width-7))
        if option.lower() == ("y") or option.lower() == ("yes"):
            export_complete = 1
            end()
   
            
            
    print ()
    print ("...Program Ending...".center(cent_width))
    print ()
    print ()
    print ()
    delete_dir(var.dir_temp)
    tasks.pause(1)
    sys.exit()    


def export_xml():
    global export_complete
    tasks.chk_file_temp(var.plu_xml)
    header()
    
    #set current date/time for directory name purposes
    set_date_time()

    #create var.dir_clean
    dir_put = (var.dir_clean + "-" + currdate + "-" + currtime)
    tasks.mk_dir(dir_put)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_temp):
       if file.endswith(".xml"):
           copy(var.dir_temp + "/" + file, dir_put + "/" + file)
           print ((file.ljust(35) + " Exported").center(cent_width))
           tasks.pause(.03)
    
    copy(var.dir_temp + "\\" + var.log_name + ".txt", dir_put + "\\" + var.log_name + ".txt")
           
    export_complete = 1
                      
    print()
    print("EXPORT COMPLETE".center(cent_width))
    tasks.pause(2)
    

       
def funct_not_supp():
    header()
    print ()
    print ("FUNCTION NOT SUPPORTED".center(cent_width))
    print ()
    print ()
    print ()
    tasks.pause(var.wait)
    

    
#Headers
def header():
    os.system("cls")
    print ()
    print ((name).center(cent_width))
    print ("David A Ray".center(cent_width))
    print ()
    
    
def import_xml():
    global export_complete
    export_complete = 0
    mk_dir_temp()
    mk_log()
    header()
   
    #set current date/time for directory name purposes
    set_date_time()

    #create backup directory
    dir_bu = (var.dir_dirty + "-" + currdate + "-" + currtime)
    tasks.mk_dir(dir_bu)
    
    #copy files from var.dir_fresh to var.dir_temp
    for file in os.listdir(var.dir_fresh):
       if file.endswith(".xml"):
           copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
           copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
           text = gui.Label(gui.Window, text=(file.ljust(35) + " Imported"))
           text.gui.pack()
           tasks.pause(.03)
           
    
    text = gui.Label(gui.Window, text="IMPORT COMPLETE")
    text.gui.pack()
    tasks.pause(2)
    
       
def list_dept():
    
    #file_temp_merch = Path(var.dir_temp + "\\" + "poscfg.xml")
    tasks.chk_file_temp("poscfg.xml")

    x = 0
    header()
    tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        name = (attributes["name"])
        
        print ((sysid.rjust(4)) + " - " + name.ljust(20))
        tasks.pause(.02)
        x += 1
        if x == (var.lines-7) or x == ((var.lines-7)*2) or x == ((var.lines-7)*3):
            print()
            tasks.pause(0)
            header()
    print()
    tasks.pause(0)

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
    print (("a folder called \"" + var.dir_dirty + "\".").center(cent_width))
    print ()
    print ("The corrected XML files are being put in".center(cent_width))
    print (("a folder valled \"" + var.dir_clean + "\".").center(cent_width))

    



        
#make var.dir_temp if needed
def mk_dir_temp():
    tasks.mk_dir(var.dir_temp)
    f = open(var.dir_temp + "\\" + "!!!READ_ME_FIRST" + ".txt","w")
    f.write(long_app + " V" + version + "\n")
    f.write("\n")
    f.write("If you found this folder then it was \n")
    f.write("only by error.  Please ***DO NOT*** \n")
    f.write("use anything in this folder or change \n")
    f.write("it in anyway.  If you go back and exit \n")
    f.write("the software properly it will resolve \n")
    f.write("this information. Thank you.\n")
    

def mk_log():
    #creates and writes to log file
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","w")
    log_currdate = dt.date.today().strftime("%m/%d/%Y")
    log_currtime = dt.datetime.now().strftime("%H:%M:%S")
    f.write(long_app + " V" + version + "\n")
    f.write("Starting Date - " + log_currdate + "\n")
    f.write("Starting Time - " + log_currtime + "\n")
    f.write("\n")
    f.close()    



#remove all id checks
def reset_idchecks():
    global export_complete, dept_tobacco_id, dept_alcohol_id

    export_complete = 0
    tasks.chk_file_temp("PLUs.xml")    
    x = 0
    file_idchk = (var.dir_temp + "/" + var.plu_xml)
    tree = et.parse(file_idchk)
    root = tree.getroot()
    tobacco = (0)
    alcohol = (0)

    for c in root:
        idchk = c.find('idChecks')    
        if idchk:
            if (c.find('idChecks')[0].attrib['sysid']) == str(2):
                #idchk_text = ("TOBACCO ID")
                tobacco += 1
            elif (c.find('idChecks')[0].attrib['sysid']) == str(1):
                #idchk_text = ("ALCOHOL ID")
                alcohol += 1
        x += 1
        print (("Checking... " + (str(x).rjust(5))).center(cent_width))
    
    header()
    
    print ()
    print (("Tobacco ID Checks: " + str(tobacco).rjust(5)).center(cent_width))
    print (("Alcohol ID Checks: " + str(alcohol).rjust(5)).center(cent_width))
    print ()
    print (("PLUs Checked: " + str(x).rjust(5)).center(cent_width))
    print ()
    print ("All ID Checks will be removed.".center(cent_width))
    print ()
    print ("Please wait while your file is being processed.".center(cent_width))
    
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)

    
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')

        global id_checks
        for tag in soup('idChecks'):
            tag.decompose()
    
    xmlin.close()
        
#    with open(outfile, 'w') as xmlout:
#        xmlout.write(soup.prettify())       
#    xmlout.close()

    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close() 
       
    set_date_time()
    header()
    print("All ID Checks Have Been Removed.".center(cent_width))
    print()
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Remove ID Checks - " + currdate + " - " + currtime + "\n")
    f.write("There were " + str(tobacco) + " Tobacco ID Checks.\n")
    f.write("There were " + str(alcohol) + " Alcohol ID Checks.\n")
    f.write("PLUs Checked: " + str(x) + "\n")
    f.write("\n")
    f.close()
    
    tasks.pause(2)

    set_tobacco_ID()

def run_pc_term():
    global export_complete


    #check is PLU file is in var.dir_temp
    tasks.chk_file_temp("PLUs.xml")

    #import data
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    #outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)

    with open (infile, "r") as xmlin:
        str_data = xmlin.readlines()        

    #count PLUs
    count_occ = len(re.findall(tag_plu, str(str_data)))
    xmlin.close()

    #run command to remove product codes
    process.remove_pcode()  
    set_date_time()
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Remove Product Codes - " + currdate + " - " + currtime + "\n")
    f.write("PLUs Checked: " + str(count_occ) + "\n")
    if count_occ <= plu_count_low:
        f.write("\n")
        f.write("\n")
        f.write ("WARNING - WARNING - WARNING - WARNING - WARNING\n")
        f.write("\n")
        f.write ("Your PLU count is lower than anticipated.  Please confirm that this number is accurate.\n")
        f.write("\n")
        f.write ("This error can be caused by using the wrong version of SMS Import/Export.  Use the Sapphire's SMS Configuration Manager to ensure you have all of the PLUs.\n")
        f.write("\n")
        f.write ("WARNING - WARNING - WARNING - WARNING - WARNING\n")
    f.write ("\n")
    f.flush()
    
    f.close()
    
    #prints on the console completion information.
    header()
    print ()
    print ("Process is Complete.".center(cent_width))
    print ()
    print (("There are " + str(count_occ) + " PLUs.").center(cent_width))
    print ()
    if count_occ <= plu_count_low:
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
    export_complete = 0
    tasks.pause(2)    
        

    
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

def set_food_stamps():
    tasks.chk_file_temp(var.plu_xml)
    tasks.chk_file_temp("poscfg.xml")
    
    tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    full_dept_list = []
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        full_dept_list.append(sysid)
            
    dept_food_stamps.sort()
    header()
    print ("  ID Set To:" + str(dept_food_stamps))
    print()
    print ("  Enter 'dept' For a List of Departments.")
    print ("  Enter 0 When Done.")
    #print (str(full_dept_list))
    add_id = input("  Choose A Department To Add Food Stamps: ")
    
    add_id_val_chk = add_id.isdigit()
    
    if add_id_val_chk:
        #if length is greater than 4 characters it is invalid
        if len(add_id) > 4:
            header()
            print ("  ID Set To:" + str(dept_food_stamps))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_food_stamps()
            
        #0 Completes Input Process
        elif add_id == "0":
            header()
            print("   Please Confirm: " + str(dept_food_stamps))
            print ()
            option = input("  Is This Correct? [Y/N]")
            if option.lower( )== ("y"):
                print ()
                for dept in dept_food_stamps:
                    print ("  Processing Department " + str(dept))
                    tasks.pause(.5)
                for dept in dept_food_stamps:
                    print ("  Adding to Department " + str(dept))
                    
                    tasks.pause(.01)
                    process.write_flags(dept, 4)
                
                tasks.pause(2)
                header()
                print ("Food Stamp Flags Have Been Added".center(cent_width))
                tasks.pause(2)
                
            else:
                set_food_stamps()
           
        else:
            #check add_id against the existing entries
            if dept_food_stamps.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_food_stamps))
                print ()
                print ("  Item Already in List.")
                tasks.pause(1)
                set_food_stamps()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_food_stamps))
                print ()
                print ("  You Have Entered an Invalid Department.")
                tasks.pause(1)
                set_food_stamps()
                
            else:
                dept_food_stamps.append(add_id)
                
                set_food_stamps()
                
    else:
        #list departments for reference
        if add_id.lower() == "dept":
            list_dept()
            set_food_stamps()
        else:
            header()
            print ("  ID Set To:" + str(dept_food_stamps))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_food_stamps()

    set_food_stamps()
    
#Set Tobacco ID Checks    
def set_tobacco_ID():

    tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    full_dept_list = []
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        full_dept_list.append(sysid)
        
    dept_tobacco_id.sort()
    header()
    print ("  ID Set To:" + str(dept_tobacco_id))
    print()
    print ("  Enter 'dept' For a List of Departments.")
    print ("  Enter 0 When Done.")
    add_id = input("  Choose A Department For Tobacco ID Check: ")
    
    add_id_val_chk = add_id.isdigit()
    
    if add_id_val_chk:
        #if length is greater than 4 characters it is invalid
        if len(add_id) > 4:
            header()
            print ("  ID Set To:" + str(dept_tobacco_id))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_tobacco_ID()
            
        #0 Completes Input Process
        elif add_id == "0":
            header()
            print("   Please Confirm: " + str(dept_tobacco_id))
            print ()
            option = input("  Is This Correct? [Y/N]")
            if option.lower( )== ("y"):
                print ()
                for dept in dept_tobacco_id:
                    print ("  Processing Department " + str(dept))
                    tasks.pause(.5)
                for dept in dept_tobacco_id:
                    print ("  Adding to Department " + str(dept))
                    
                    tasks.pause(.01)
                    process.write_id_chk(dept, 2)
                
                tasks.pause(2)
                header()
                print ("ID Checks Have Been Added".center(cent_width))
                tasks.pause(2)
                set_alcohol_ID()
            else:
                set_tobacco_ID()
           
        else:
            #check add_id against the existing entries
            if dept_tobacco_id.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_tobacco_id))
                print ()
                print ("  Item Already in List.")
                tasks.pause(1)
                set_tobacco_ID()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_tobacco_id))
                print ()
                print ("  You Have Entered an Invalid Department.")
                tasks.pause(1)
                set_tobacco_ID()
                
            else:
                dept_tobacco_id.append(add_id)
                
                set_tobacco_ID()
                
    else:
        #list departments for reference
        if add_id.lower() == "dept":
            list_dept()
            set_tobacco_ID()
        else:
            header()
            print ("  ID Set To:" + str(dept_tobacco_id))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_tobacco_ID()

    set_tobacco_ID()

#Set Alcohol ID Checks    
def set_alcohol_ID():

    tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    full_dept_list = []
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        full_dept_list.append(sysid)

    dept_alcohol_id.sort()
    header()
    print ("  ID Set To:" + str(dept_alcohol_id))
    print()
    print ("  Enter 'dept' For a List of Departments.")
    print ("  Enter 0 When Done.")
    add_id = input("  Choose A Department For Alcohol ID Check: ")
    
    add_id_val_chk = add_id.isdigit()
    
    if add_id_val_chk:
        #if length is greater than 4 characters it is invalid
        if len(add_id) > 4:
            header()
            print ("  ID Set To:" + str(dept_alcohol_id))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_alcohol_ID()
            
        #0 Completes Input Process
        elif add_id == "0":
            header()
            print("   Please Confirm: " + str(dept_alcohol_id))
            print ()
            option = input("  Is This Correct? [Y/N]")
            if option.lower( )== ("y"):
                print ()
                for dept in dept_alcohol_id:
                    print ("  Processing Department " + str(dept))
                    tasks.pause(.5)
                for dept in dept_alcohol_id:
                    print ("  Adding to Department " + str(dept))
                    
                    tasks.pause(.01)
                    process.write_id_chk(dept, 1)
                
                tasks.pause(2)    
                header()
                print ("ID Checks Have Been Added".center(cent_width))
                tasks.pause(2)
                
            else:
                set_alcohol_ID()
           
        else:
            #check add_id against the existing entries
            if dept_alcohol_id.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_alcohol_id))
                print ()
                print ("  Item Already in List.")
                tasks.pause(1)
                set_alcohol_ID()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_alcohol_id))
                print ()
                print ("  You Have Entered an Invalid Department.")
                tasks.pause(1)
                set_alcohol_ID()
                
            else:
                dept_alcohol_id.append(add_id)
                
                set_alcohol_ID()
        
    else:
        #list departments for reference
        if add_id.lower() == "dept":
            list_dept()
            set_alcohol_ID()
        else:
            header()
            print ("  ID Set To:" + str(dept_alcohol_id))
            print()
            print ("  Invalid Entry.")
            tasks.pause(1)
            set_alcohol_ID()

    set_alcohol_ID()

#run commands
if __name__ == "__main__":
    if os.path.exists(var.dir_temp):
        delete_dir(var.dir_temp)
    mk_dir(var.dir_fresh)
    logo()
    tasks.pause(var.wait)
    
    
    