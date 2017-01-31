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
version = "0.06.00F"
email = "David@DREAM-Enterprise.com"
name = long_app + "  V" + version
dir_fresh = "Put_XMLs_Here"
dir_clean = "Processed_XMLs"
dir_dirty = "BackUp_XMLs"
dir_temp = "TEMP"
plu_xml = "PLUs.xml"
plu_xml_2 = "PLUs_mod.xml"
log_name = "!PC_Term Report"
tag = "pcode"
value = 0
count_tag = "<domain:PLU>"
count_low = 250
count_plu = 0
tag_plu = "<domain:PLU>"
var_not_found = 0
export_complete = 1
fs = "Not Food Stamp"
dept_tobacco_id = []
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
menu_07 = "7 - Function Not Supported"
menu_08 = "8 - Function Not Supported"
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
    
    #full_dir_temp = os.path.abspath(os.path.join(dir_temp))
    #print (full_dir_temp)
    
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
        #####isallowfs = (attributes["isAllowFS"])
        
        #if isallowfs == 0:
        #    fs = "Not Food Stamp"
        #elif isallowfs == 1:
        #    fs = "Food Stamp"
        
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
        reset_idchecks()
    elif option == ("7"):
        funct_not_supp()
    elif option == ("8"):
        funct_not_supp()
    elif option == ("9"):
        chk_store_backup()
    else:
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
'''
        
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


#remove all product codes
def remove_pcode():
    #global x
    x=0
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

#remove all id checks
def reset_idchecks():
    global export_complete, dept_tobacco_id
    dept_tobacco_id = []
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
        #header ()
        #print ()
        #print ("Processing...  Please wait a moment".center(cent_width))
        #print ()

        #idchk_text = ""
        #os.system("pause")
        if idchk:
            if (c.find('idChecks')[0].attrib['sysid']) == str(1):
                #idchk_text = ("TOBACCO ID")
                tobacco += 1
            elif (c.find('idChecks')[0].attrib['sysid']) == str(2):
                #idchk_text = ("ALCOHOL ID")
                alcohol += 1
        #print (root[x][0].text + " " + (root[x][3].text).rjust(4) + " " + root[x][2].text.ljust(27) + " " + idchk_text)
        #sleep(.000005)
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
    
    with open(file_idchk) as xmlin:
        soup = bs(xmlin, 'xml')

        global id_checks
        id_checks = [ tag.extract() for tag in soup('idChecks') ]
        
    with open(file_idchk, 'w') as xmlout:
        xmlout.write(soup.prettify())
    set_date_time()
    header()
    print("All ID Checks Have Been Removed.".center(cent_width))
    print()
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Remove ID Checks - " + currdate + " - " + currtime + "\n")
    f.write("There were " + str(tobacco) + " Tobacco ID Checks.\n")
    f.write("There were " + str(alcohol) + " Alcohol ID Checks.\n")
    f.write("PLUs Checked: " + str(x) + "\n")
    f.close()
    
    sleep(2)
    set_tobacco_ID()


def run_pc_term():
    global export_complete


    #check is PLU fole is in dir_fresh
    chk_file_temp("PLUs.xml")
    #mk_dir_temp()
    
    #copy PLUs to TEMP folder
    #copy(dir_fresh + "/" + plu_xml, dir_temp + "/" + plu_xml)
    
    #import data
    with open (dir_temp + "/" + plu_xml, "r") as raw_data:
        str_data = raw_data.readlines()        
    #count PLUs
    count_occ = len(re.findall(count_tag, str(str_data)))

    #run command to remove product codes
    remove_pcode()  
    set_date_time()
    f = open(dir_temp + "\\" + log_name + ".txt","a")
    f.write("Remove Product Codes - " + currdate + " - " + currtime + "\n")
    f.write("PLUs Checked: " + str(count_occ) + "\n")
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
    export_complete = 0
    sleep(2)    
    main_menu()    

    
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")


#Set Tobacco ID Checks    
def set_tobacco_ID():
    
    tree = et.parse(dir_temp + "//" + "poscfg.xml")
    root = tree.getroot()
    
    full_dept_list = []
    for dept in root.iter('department'):
        attributes = (dept.attrib)
        sysid = (attributes["sysid"])
        full_dept_list.append(sysid.zfill(4))
        
    dept_tobacco_id.sort()
    header()
    print ("  ID Set To:" + str(dept_tobacco_id))
    print()
    print ("  Enter 'dept' For a List of Departments.")
    print ("  Enter 0 When Done.")
    #print (str(full_dept_list))
    add_id = input("  Choose A Department For Tobacco ID Check: ")
    
    #print (add_id.isdigit())
    #os.system("pause")
    
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
                file_idchk = (dir_temp + "/" + plu_xml)
                subchild_tobacco = '<idChecks>\n<domain:idCheck sysid="1"/>\n</idChecks>'
                #subchild_tobacco = id_checks.pop(0)
                #print (subchild_tobacco)
                #os.system("pause")
                for dept in dept_tobacco_id:
                    print ("  Processing Department " + str(dept))
                    sleep(.5)
                for dept in dept_tobacco_id:
                    print ("  Adding to " + str(dept))
                    sleep(.01)
                    write_id_chk('0011')
                    
                header()
                print ("  ID Checks Have Been Added")
                sleep(2)
                main_menu()
                sleep(2)
            else:
                set_tobacco_ID()
           
           
        else:
            add_id = add_id.zfill(4)
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
    

    
    #################Start CommandLineLuser Code                    
    
def write_id_chk(dept):

    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml_2)
    
    subchild_tobacco = ('<idChecks><domain:idCheck sysid="1"/></idChecks>')

    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')
    
    for department in soup('department', string=dept):
        print (department)
        department.find_parent('PLU').append(str(subchild_tobacco))
    
    with open(outfile, 'w') as xmlout:
        xmlout.write(soup.prettify())
    
    ######################End CommandLineLuser Code                        


    
    
#run commands
if __name__ == "__main__":
    if os.path.exists(dir_temp):
        delete_dir(dir_temp)
        mk_dir(dir_fresh)
        logo()
        sleep(wait)
        
        main_menu()

    