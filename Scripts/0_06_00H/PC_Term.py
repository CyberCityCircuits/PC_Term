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
from bs4 import BeautifulSoup as bs
import re

#set varibles
application = "PC_Term"
long_app = "Product Code Terminator"
version = "0.06.00H"
email = "David@DREAM-Enterprise.com"
name = long_app + "  V" + version
dir_fresh = "Put_XMLs_Here"
dir_clean = "Processed_XMLs"
dir_dirty = "BackUp_XMLs"
dir_temp = "TEMP"
plu_xml = "PLUs.xml"
plu_xml_2 = "PLUs_mod.xml"
log_name = "!PC_Term Report"

value = 0
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
wait = 3.0
width = 60
lines = 35
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
menu_01 = "1 - Import Backup from " + dir_fresh
menu_02 = "2 - Save data to " + dir_clean
menu_03 = "3 - List All Departments" 
menu_04 = "4 - Function Not Supported"
menu_05 = "5 - Remove Product Codes from PLU file"
menu_06 = "6 - Reset All ID Checks"
menu_07 = "7 - Remove All Food Stamp Checks"
menu_08 = "8 - Set All Food Stamp Checks"
menu_09 = "9 - Check Store Backup"

#define commands


       
#checks if files exist in dir_fresh by attribute        
def chk_file_fresh(title, file_name):
    global var_not_found
    if not os.path.isfile(dir_fresh + "//" + file_name):
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Not Found"))
        var_not_found = 1
    else:
        print ((" " + title.ljust(15) + " " + file_name.ljust(15) + " - File Exists"))
        
#checks if file exists in dir_temp
def chk_file_temp(file_name):
    if not Path(dir_temp + "/" + file_name).is_file():
        header()
        print ()
        print ("FILE NOT FOUND".center(cent_width))
        print ()
        print (("Please move your store backup XMLs to").center(cent_width))
        print (("the directory named " + dir_fresh + " and then").center(cent_width))
        print (("use the option to IMPORT YOUR BACKUP.").center(cent_width))
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

        
#check to see if files are present in dir_fresh
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
        else:
            main_menu()
            
    print ()
    print ("...Program Ending...".center(cent_width))
    print ()
    print ()
    print ()
    delete_dir(dir_temp)
    sleep(1)
    sys.exit()    


def export_xml():
    global export_complete
    chk_file_temp(plu_xml)
    header()
    
    #set current date/time for directory name purposes
    set_date_time()

    #create dir_clean
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    mk_dir(dir_put)
    
    #copy files from dir_fresh to dir_temp
    for file in os.listdir(dir_temp):
       if file.endswith(".xml"):
           copy(dir_temp + "/" + file, dir_put + "/" + file)
           print ((file.ljust(35) + " Exported").center(cent_width))
           sleep(.03)
    
    copy(dir_temp + "\\" + log_name + ".txt", dir_put + "\\" + log_name + ".txt")
           
    export_complete = 1
                      
    print()
    print("EXPORT COMPLETE".center(cent_width))
    sleep(2)
    main_menu()

       
def funct_not_supp():
    header()
    print ()
    print ("FUNCTION NOT SUPPORTED".center(cent_width))
    print ()
    print ()
    print ()
    sleep(wait)
    main_menu()

    
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
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    mk_dir(dir_bu)
    
    #copy files from dir_fresh to dir_temp
    for file in os.listdir(dir_fresh):
       if file.endswith(".xml"):
           copy(dir_fresh + "/" + file, dir_temp + "/" + file)
           copy(dir_fresh + "/" + file, dir_bu + "/" + file)
           print ((file.ljust(35) + " Imported").center(cent_width))
           sleep(.03)
           
    print()
    print("IMPORT COMPLETE".center(cent_width))
    sleep(2)
    main_menu()
       
def list_dept():
    
    #file_temp_merch = Path(dir_temp + "\\" + "poscfg.xml")
    chk_file_temp("poscfg.xml")

    x = 0
    header()
    tree = et.parse(dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        name = (attributes["name"])
        
        print ((sysid.rjust(4)) + " - " + name.ljust(20))
        sleep(.02)
        x += 1
        if x == (lines-7) or x == ((lines-7)*2) or x == ((lines-7)*3):
            print()
            os.system("pause")
            header()
    print()
    os.system("pause")

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

#main menu
def main_menu():
    global dept_food_stamps, dept_tobacco_id, dept_alcohol_id
    
    header()
    print ()
    print ()
    print ("  " + menu_00)
    print()
    print ("  " + menu_01)
    print()
    print ("  " + menu_02)
    print()
    print ("  " + menu_03)
    print()
    print ("  " + menu_04)
    print()
    print ("  " + menu_05)
    print()
    print ("  " + menu_06)
    print()
    print ("  " + menu_07)
    print()
    print ("  " + menu_08)
    print()
    print ("  " + menu_09)
    print()
    
    option = input("  Enter Your Selection: ")
    if option == ("0"):
        end()
    elif option == ("1"):
        import_xml()
    elif option == ("2"):
        export_xml()
    elif option == ("3"):
        list_dept()
        main_menu()
    elif option == ("4"):
        funct_not_supp()
    elif option == ("5"):
        run_pc_term()
    elif option == ("6"):
        dept_alcohol_id = []
        dept_tobacco_id = []    
        reset_idchecks()
    elif option == ("7"):
        process_remove_fs()
    elif option == ("8"):
        dept_food_stamps = []
        set_food_stamps()
    elif option == ("9"):
        chk_store_backup()
    else:
        main_menu()    
    
#make directories as needed
def mk_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        
#make dir_temp if needed
def mk_dir_temp():
    if not os.path.exists(dir_temp):
        mk_dir(dir_temp)
    f = open(dir_temp + "\\" + "!!!READ_ME_FIRST" + ".txt","w")
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
    f = open(dir_temp + "\\" + log_name + ".txt","w")
    log_currdate = dt.date.today().strftime("%m/%d/%Y")
    log_currtime = dt.datetime.now().strftime("%H:%M:%S")
    f.write(long_app + " V" + version + "\n")
    f.write("Starting Date - " + log_currdate + "\n")
    f.write("Starting Time - " + log_currtime + "\n")
    f.write("\n")
    f.close()    

#Removed all Food Stamp Tags.  Verified Working.    
def process_remove_fs():
    x = 0
    chk_file_temp("PLUs.xml")
    set_date_time()
    header()
    print ("Processing...".center(cent_width))
    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml)
    
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')

    for tag in soup(attrs={'sysid': '4'}):
        x += 1
        tag.decompose()
    
    #print (soup)    
    #os.system('pause')
    
    xmlin.close()
    
    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close()
    
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Remove Food Stamp Flags " + currdate + " " + currtime + "\n")
    f.write("Removed Flag Count " + str(x) + "\n")
    f.write("\n")
    f.close()   

    
    header()
    print ("All Food Stamp Tags Removed".center(cent_width))
    print (("Removed " + str(x) + " Food Stamp Tags").center(cent_width))
    sleep(3)
    
    main_menu()

#remove all product codes
def process_remove_pcode():
    x=0
    tag = "pcode"
    tree = et.parse(dir_temp + "/" + plu_xml)
    root = tree.getroot()
    for xml_tag in root.iter(tag):
        xml_tag.text = str(value)
    tree.write(dir_temp + "/" + plu_xml,encoding="UTF-8",xml_declaration=True)
    
    for c in root:
        x += 1
        print (("Checking... " + (str(x).rjust(5))).center(cent_width))
        #sleep(.00001)
    print ("  Processing...")
    sleep(2)



def process_write_flags(dept, value):
    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml)
    
    set_date_time()
    
    x=0
    if value == 1:
        flag_value = ('domain:flag sysid="1"')
    elif value == 2:
        flag_value = ('domain:flag sysid="2"')
    elif value == 3:
        flag_value = ('domain:flag sysid="3"')    
    elif value == 4:
        flag_value = ('domain:flag sysid="4"')
    else:
        #error logging
        header()
        print ("There was a major error.".center(cent_width))
        print ("Please send the PC_Term_Report to David Ray.".center(cent_width))
        
        set_date_time()
        
        f = open(dir_temp + "\\" + log_name + ".txt","a")
        f.write("Error writing flags. " + currdate + " " + currtime + "\n")
        f.write("Location - process_write_flags\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
        print()
        print()
        print()
        os.system("pause")
        main_menu()

    
    #Process for actually checking if flag already exists and then adding it as needed.    
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')
        new_tag = soup.new_tag("flags")
        
    for plu in soup.find_all('PLU'):
        xmlin_dept = plu.department.get_text().strip()
        
        #CHECK TO SEE IF DEPT MATCHES.
        if xmlin_dept.lstrip("0") == dept.lstrip("0"):
            new_tag = soup.new_tag("flags")
            if not plu.find('flags'):
                plu.append(new_tag)

            if not plu.find('flag', attrs={'sysid': 4}):
                new_tag = soup.new_tag(flag_value)
                plu.flags.append(new_tag)

                x += 1
    
    xmlin.close()
        
#    with open(outfile, 'w') as xmlout:
#        xmlout.write(soup.prettify())
#    xmlout.close()

    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close()
    
    
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Writing Food Stamps " + currdate + " " + currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    print ("  " + str(x) + " Food Stamp flags added to Department " + str(dept))
    
    sleep(2)
    
def process_write_id_chk(dept, value):
    x = 0
    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml)
       
    if value == 1:
        idchk_value = ('domain:idCheck sysid="1"')
    elif value == 2:
        idchk_value = ('domain:idCheck sysid="2"')
    else:
        header()
        print ("There was a major error.".center(cent_width))
        print ("Please send the PC_Term_Report to David Ray.".center(cent_width))
        
        set_date_time()
        
        f = open(dir_temp + "\\" + log_name + ".txt","a")
        f.write("Error writing ID checks. " + currdate + " " + currtime + "\n")
        
        f.write("Location - process_write_id_chk\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
        print()
        print()
        print()
        os.system("pause")
        main_menu()
        
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')
    
    for department in soup.find_all('department'):
        xmlin_dept = department.get_text().strip()
        #print (xmlin_dept)
        if xmlin_dept.lstrip("0") == dept.lstrip("0"):
            x+=1
            
            new_tag = soup.new_tag("idChecks")
            department.find_parent('PLU').append(new_tag)
            department.find_parent('PLU').idChecks.append(soup.new_tag(idchk_value))
            
    xmlin.close()
        
#    with open(outfile, 'w') as xmlout:
#        xmlout.write(soup.prettify())   
#    xmlout.close()
    
    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close()

    set_date_time()
    
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Writing ID Checks " + currdate + " " + currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    
    print ("  " + str(x) + " ID Checks added to Department " + str(dept))
    
#remove all id checks
def reset_idchecks():
    global export_complete, dept_tobacco_id, dept_alcohol_id

    export_complete = 0
    chk_file_temp("PLUs.xml")    
    x = 0
    file_idchk = (dir_temp + "/" + plu_xml)
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
    
    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml)

    
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
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Remove ID Checks - " + currdate + " - " + currtime + "\n")
    f.write("There were " + str(tobacco) + " Tobacco ID Checks.\n")
    f.write("There were " + str(alcohol) + " Alcohol ID Checks.\n")
    f.write("PLUs Checked: " + str(x) + "\n")
    f.write("\n")
    f.close()
    
    sleep(2)

    set_tobacco_ID()

def run_pc_term():
    global export_complete


    #check is PLU file is in dir_temp
    chk_file_temp("PLUs.xml")

    #import data
    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    #outfile = os.path.abspath(dir_temp + "/" + plu_xml)

    with open (infile, "r") as xmlin:
        str_data = xmlin.readlines()        

    #count PLUs
    count_occ = len(re.findall(tag_plu, str(str_data)))
    xmlin.close()

    #run command to remove product codes
    process_remove_pcode()  
    set_date_time()
    f = open(dir_temp + "\\" + log_name + ".txt","a")
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
    sleep(2)    
    main_menu()    

    
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")

def set_food_stamps():
    chk_file_temp(plu_xml)
    chk_file_temp("poscfg.xml")
    
    tree = et.parse(dir_temp + "//" + "poscfg.xml")
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
            sleep(1)
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
                    sleep(.5)
                for dept in dept_food_stamps:
                    print ("  Adding to Department " + str(dept))
                    
                    sleep(.01)
                    process_write_flags(dept, 4)
                
                sleep(2)
                header()
                print ("Food Stamp Flags Have Been Added".center(cent_width))
                sleep(2)
                main_menu()
            else:
                set_food_stamps()
           
        else:
            #check add_id against the existing entries
            if dept_food_stamps.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_food_stamps))
                print ()
                print ("  Item Already in List.")
                sleep(1)
                set_food_stamps()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_food_stamps))
                print ()
                print ("  You Have Entered an Invalid Department.")
                sleep(1)
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
            sleep(1)
            set_food_stamps()

    set_food_stamps()
    
#Set Tobacco ID Checks    
def set_tobacco_ID():

    tree = et.parse(dir_temp + "//" + "poscfg.xml")
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
            sleep(1)
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
                    sleep(.5)
                for dept in dept_tobacco_id:
                    print ("  Adding to Department " + str(dept))
                    
                    sleep(.01)
                    process_write_id_chk(dept, 2)
                
                sleep(2)
                header()
                print ("ID Checks Have Been Added".center(cent_width))
                sleep(2)
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
                sleep(1)
                set_tobacco_ID()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_tobacco_id))
                print ()
                print ("  You Have Entered an Invalid Department.")
                sleep(1)
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
            sleep(1)
            set_tobacco_ID()

    set_tobacco_ID()

#Set Alcohol ID Checks    
def set_alcohol_ID():

    tree = et.parse(dir_temp + "//" + "poscfg.xml")
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
            sleep(1)
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
                    sleep(.5)
                for dept in dept_alcohol_id:
                    print ("  Adding to Department " + str(dept))
                    
                    sleep(.01)
                    process_write_id_chk(dept, 1)
                
                sleep(2)    
                header()
                print ("ID Checks Have Been Added".center(cent_width))
                sleep(2)
                main_menu()
            else:
                set_alcohol_ID()
           
        else:
            #check add_id against the existing entries
            if dept_alcohol_id.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_alcohol_id))
                print ()
                print ("  Item Already in List.")
                sleep(1)
                set_alcohol_ID()
            #check add_id against a list of known departments    
            elif not full_dept_list.count(add_id):
                header()
                print ("  ID Set To:" + str(dept_alcohol_id))
                print ()
                print ("  You Have Entered an Invalid Department.")
                sleep(1)
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
            sleep(1)
            set_alcohol_ID()

    set_alcohol_ID()

#run commands
if __name__ == "__main__":
    if os.path.exists(dir_temp):
        delete_dir(dir_temp)
    mk_dir(dir_fresh)
    logo()
    sleep(wait)
    
    main_menu()
    