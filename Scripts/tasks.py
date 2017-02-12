# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:14:01 2017

@author: admin
"""

import var

import os, re
import datetime as dt
from time import sleep
from shutil import copyfile
from shutil import rmtree as rm_dir
from pathlib import Path
from bs4 import BeautifulSoup as bs
import lxml.etree as et

#from tkinter import *
from tkinter import messagebox, Label
from tkinter import simpledialog



#set varibles
export_complete = 1

currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")


    
#checks if file exists in var.dir_temp
def chk_file_temp(file_name):
    if not Path(var.dir_temp + "/" + file_name).is_file():
        msg_error("T04: Check Error\nFile Not Found. \n ")   


#copy files
def copy(fn1,fn2):
    if os.path.isfile(fn1):
        copyfile(fn1,fn2)
    else:
        msg_error("T03: Copy Error\nFile Doesn't Exit")
       
        
#delete a directory
def delete_dir(dir_name):
    if os.path.exists(dir_name):
        rm_dir(dir_name)
    #else:
    #    msg_error("T01: Delete Error\nDirectory Doesn't Exist")
        
#delete file
def delete_file(file_name):
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        msg_error("T02: Delete Error\nFile Doesn't Exit")

'''
def import_xml():
    global export_complete
    export_complete = 0
    
    if not Path(var.dir_fresh + "/" + var.plu_xml).is_file():
        msg_error("T05: Import Error\nFile Not Found.\n\nPlease Place Your Dataset\nIn The Folder Named\n" + var.dir_fresh)   
    
    else:
        mk_dir(var.dir_temp)
        mk_log()
        
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
        msg("Import Complete\n\nYour Back Up Is In a Folder\nNamed " + var.dir_dirty)
        
'''
        
def export_xml():
    global export_complete
    if Path(var.dir_temp + "/" + var.plu_xml).is_file():
            
        #set current date/time for directory name purposes
        set_date_time()
    
        #create var.dir_clean
        dir_put = (var.dir_clean + "-" + currdate + "-" + currtime)
        mk_dir(dir_put)
        
        #copy files from var.dir_temp var.dir_put
        for file in os.listdir(var.dir_temp):
           if file.endswith(".xml"):
               copy(var.dir_temp + "/" + file, dir_put + "/" + file)
                   
        set_date_time()
        copy(var.dir_temp + "\\" + var.log_name + ".txt", dir_put + "\\" + var.log_name + ".txt")
               
        export_complete = 1
                          
        msg("Export Complete\n\nYour Export Is In a Folder\nnamed " + var.dir_clean)
        
    else:
        msg_error("T06: Export Error\nFile Not Found. \n ")   

        
def import_xml():
    
    if not Path(var.dir_fresh + "/" + var.plu_xml).is_file():
        msg_error("T05: Import Error\nFile Not Found.\n\nPlease Place Your Dataset\nIn The Folder Named\n" + var.dir_fresh)   
    
    else:
        mk_dir(var.dir_temp)
        mk_log()
        
        set_date_time()
    
        dir_bu = (var.dir_dirty + "-" + currdate + "-" + currtime)
        mk_dir(dir_bu)
        
        for file in os.listdir(var.dir_fresh):
           if file.endswith(".xml"):
               copy(var.dir_fresh + "/" + file, var.dir_temp + "/" + file)
               copy(var.dir_fresh + "/" + file, dir_bu + "/" + file)
        msg("Import Complete\n\nYour Back Up Is In a Folder\nNamed " + var.dir_dirty)
   
        
def msg(text):
    messagebox.showinfo(var.app_name, text)
    
def msg_error(text):
    messagebox.showerror(var.app_name, text)
    
#set wait command
def pause(value):
    if value == 0:   #if 0 is entered it creates a press any key prompt.
        os.system("pause")
    elif int(value):
        sleep(value)


#set date and time        
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")
        
        
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

#remove all product codes
def process_remove_pcode():
    x=0
    tag = "pcode"
    pcode_value = 0
    tree = et.parse(var.dir_temp + "/" + var.plu_xml)
    root = tree.getroot()
    for xml_tag in root.iter(tag):
        xml_tag.text = str(pcode_value)
    tree.write(var.dir_temp + "/" + var.plu_xml,encoding="UTF-8",xml_declaration=True)
    
    for c in root:
        x += 1
        
        
#Removed all Food Stamp Tags.  Verified Working.    
def remove_fs():
    x = 0
    #check is PLU file is in dir_temp
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T08: Check Error\nFile Not Found. \n ")   
    else:
        msg("Removing All Food Stamp Checks.\n\n"
            "This Will Take Several Moments.\n\nPlease Be Patient.")
        set_date_time()
        infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
        outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
        
        with open(infile) as xmlin:
            soup = bs(xmlin, 'xml')
    
        for tag in soup(attrs={'sysid': '4'}):
            x += 1
            tag.decompose()
    
        xmlin.close()
        
        new_data = str(soup)
        plu_new = open(outfile,"w")
        plu_new.write(new_data)
        plu_new.close()
        
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Remove Food Stamp Flags " + currdate + " " + currtime + "\n")
        f.write("Removed Flag Count " + str(x) + "\n")
        f.write("\n")
        f.close()   
    
        msg("All Food Stamp Tags Removed\n\nRemoved " + str(x) + " Food Stamp Tags")
        
    

    
def run_pc_term():
    global export_complete

    #check is PLU file is in dir_temp
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T07: Check Error\nFile Not Found. \n ")   
    else:
    
        #import data
        infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
        #outfile = os.path.abspath(dir_temp + "/" + plu_xml)
    
        with open (infile, "r") as xmlin:
            str_data = xmlin.readlines()        
    
        #count PLUs
        count_occ = len(re.findall(var.tag_plu, str(str_data)))
        xmlin.close()
    
        #run command to remove product codes
        process_remove_pcode()  
        set_date_time()
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Remove Product Codes - " + currdate + " - " + currtime + "\n")
        f.write("PLUs Checked: " + str(count_occ) + "\n")
        if count_occ <= var.plu_count_low:
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
        
        msg("Process is Complete.\n\n" 
        "There are " + str(count_occ) + " PLUs.")
        
        if count_occ <= var.plu_count_low:
            msg_error("Your PLU count is lower than anticipated.\n"
            "Please confirm that this number is accurate.\n\n"
            "This error can be caused by using the wrong\n"
            "version of SMS Import/Export.  Use the\n"
            " Sapphire's SMS Configuration Manager to\n"
            "ensure you have all of the PLUs.")
        
        export_complete = 0
            
    

def write_flags(dept, value):
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    
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
        msg_error("There Was a Major Error.\n\nPlease Send The PC_Term_Report\nTo David Ray.")
        
        set_date_time()
        
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Error writing flags. " + currdate + " " + currtime + "\n")
        f.write("Location - process_write_flags\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
    
    #Process for actually checking if flag already exists and then adding it as needed.    
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')
        new_tag = soup.new_tag("flags")
        
    for plu in soup.find_all('PLU'):
        xmlin_dept = plu.department.get_text().strip()
        
        #CHECK TO SEE IF DEPT MATCHES.
        if xmlin_dept.lstrip("0") == str(dept).lstrip("0"):
            new_tag = soup.new_tag("flags")
            if not plu.find('flags'):
                plu.append(new_tag)

            if not plu.find('flag', attrs={'sysid': 4}):
                new_tag = soup.new_tag(flag_value)
                plu.flags.append(new_tag)

                x += 1
    
    xmlin.close()
    
    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close()
    
    
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Writing Food Stamps " + currdate + " " + currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    #msg(str(x) + " Food Stamp flags added to Department " + str(dept))
        
    var.fs_count += x    
    
    
def write_id_chk(dept, value):
    x = 0
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
       
    if value == 1:
        idchk_value = ('domain:idCheck sysid="1"')
    elif value == 2:
        idchk_value = ('domain:idCheck sysid="2"')
    else:
        msg_error("There Was a Major Error.\n\n"
                  "Please Send The PC_Term_Report\nTo David Ray.")
        
        set_date_time()
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Error writing ID checks. " + currdate + " " + currtime + "\n")
        f.write("Location - process_write_id_chk\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
        
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')
    
    for department in soup.find_all('department'):
        xmlin_dept = department.get_text().strip()
        if xmlin_dept.lstrip("0") == str(dept).lstrip("0"):
            x+=1
            
            new_tag = soup.new_tag("idChecks")
            department.find_parent('PLU').append(new_tag)
            department.find_parent('PLU').idChecks.append(soup.new_tag(idchk_value))
            
    xmlin.close()
        
    new_data = str(soup)
    plu_new = open(outfile,"w")
    plu_new.write(new_data)
    plu_new.close()

    set_date_time()
    
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Writing ID Checks " + currdate + " " + currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    if value == 1:
        var.tobacco_id_count += x
    elif value == 2:
        var.tobacco_id_count += x
    
    
#remove all id checks
def remove_idchecks():
    global export_complete

    export_complete = 0
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T10: Check Error\nFile Not Found. \n ")   
    else:
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
                
        msg("Tobacco ID Checks: " + str(tobacco) + "\n"
            "Alcohol ID Checks: " + str(alcohol) + "\n\n"
            "PLUs Checked: " + str(x) + "\n\n"
            "All ID Checks will be removed.\n"
            "Please wait while your file is being processed.\n"
            "Please be patient.")
        
        infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
        outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    
        
        with open(infile) as xmlin:
            soup = bs(xmlin, 'xml')
    
            global id_checks
            for tag in soup('idChecks'):
                tag.decompose()
        
        xmlin.close()
    
        new_data = str(soup)
        plu_new = open(outfile,"w")
        plu_new.write(new_data)
        plu_new.close() 
           
        set_date_time()
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Remove ID Checks - " + currdate + " - " + currtime + "\n")
        f.write("There were " + str(tobacco) + " Tobacco ID Checks.\n")
        f.write("There were " + str(alcohol) + " Alcohol ID Checks.\n")
        f.write("PLUs Checked: " + str(x) + "\n")
        f.write("\n")
        f.close()
        
        msg("All ID Checks Have Been Removed.")

        
#Set Tobacco ID Checks    
def set_tobacco_ID():
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T11: Check Error\nFile Not Found. \n ")   
    else:
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root = tree.getroot()
        
        full_dept_list = []
        for dept in root.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            full_dept_list.append(sysid)
         
        #msg(var.dept_list)
            
        var.dept_tobacco_id.sort()
        add_id = simpledialog.askinteger("Tobacco ID Checks", 
             "ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
             "Enter '0' to End.\n"
             "Use '-' to Remove an Entry.\n"
             "What Department Would You Like to Add?")
           
        #0 Completes Input Process
        if add_id == 0:
            result = messagebox.askquestion("Confirm", 
                                            "Please Confirm: " + str(var.dept_tobacco_id), 
                                            icon="question")
            if result == "yes":
                for dept in var.dept_tobacco_id:
                    msg("Writing ID Checks to Department " + str(dept) + "\n"
                        "Please Be Patient.")
                    write_id_chk(int(dept), 2)
                    
                msg("Tobacco ID Checks Have Been Added")
            else:
                set_tobacco_ID()


        #Remove Entry From Department List                
        elif int(add_id) < 0:
            
            #msg("Remove Dept" + str(add_id))
            
            add_id = str(abs(add_id))
            
            #msg("This Should Be Absolute Value" + str(add_id))
            
            if not (var.dept_list).count(str(add_id)):
                msg_error("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                          "T14 - You Have Entered an Invalid Department.")
                set_tobacco_ID()
          
            elif not (var.dept_tobacco_id).count(int(add_id)):
                msg_error("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                          "T15 - You Have Entered an Invalid Department.")
                set_tobacco_ID()
               
            else:
                #msg("Removing Department " + str(add_id))
                var.dept_tobacco_id.remove(int(add_id))
                msg("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                    "Department " + add_id + " Removed.")
                set_tobacco_ID()
            
         
        #check add_id against the existing entries
        elif (var.dept_tobacco_id).count(add_id):
            msg_error("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                      "Item Already On List")
            set_tobacco_ID()
            
        #check add_id against a list of known departments    
        elif not (var.dept_list).count(str(add_id)):
            msg_error("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                      "You Have Entered an Invalid Department.")
            set_tobacco_ID()
            
        else:
            var.dept_tobacco_id.append(add_id)
            
            set_tobacco_ID()
        

#Set alcohol ID Checks    
def set_alcohol_ID():
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T12: Check Error\nFile Not Found. \n ")   
    else:
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root = tree.getroot()
        
        full_dept_list = []
        for dept in root.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            full_dept_list.append(sysid)
         
        #msg(var.dept_list)
            
        var.dept_alcohol_id.sort()
        add_id = simpledialog.askinteger("Alcohol ID Checks", 
             "ID Set To:" + str(var.dept_alcohol_id) + "\n\n"
             "Enter '0' to End.\n"
             "What Department Would You Like to Add?")
           
        #0 Completes Input Process
        if add_id == 0:
            result = messagebox.askquestion("Confirm", 
                                            "Please Confirm: " + str(var.dept_alcohol_id), 
                                            icon="question")
            if result == "yes":
                for dept in var.dept_alcohol_id:
                    msg("Writing ID Checks to Department " + str(dept) + "\n"
                        "Please Be Patient.")
                    write_id_chk(int(dept), 1)
                    
                msg("Alcohol ID Checks Have Been Added")
            else:
                set_alcohol_ID()
                
        #Remove Entry From Department List                
        elif int(add_id) < 0:
            
            #msg("Remove Dept" + str(add_id))
            
            add_id = str(abs(add_id))
            
            #msg("This Should Be Absolute Value" + str(add_id))
            
            if not (var.dept_list).count(str(add_id)):
                msg_error("ID Set To:" + str(var.dept_alcohol_id) + "\n\n"
                          "T14 - You Have Entered an Invalid Department.")
                set_alcohol_ID()
          
            elif not (var.dept_alcohol_id).count(int(add_id)):
                msg_error("ID Set To:" + str(var.dept_alcohol_id) + "\n\n"
                          "T15 - You Have Entered an Invalid Department.")
                set_alcohol_ID()
               
            else:
                #msg("Removing Department " + str(add_id))
                var.dept_alcohol_id.remove(int(add_id))
                msg("ID Set To:" + str(var.dept_tobacco_id) + "\n\n"
                    "Department " + add_id + " Removed.")
                set_alcohol_ID()
            
             
        #check add_id against the existing entries
        elif (var.dept_alcohol_id).count(add_id):
            msg_error("ID Set To:" + str(var.dept_alcohol_id) + "\n\n"
                      "Item Already On List")
            set_alcohol_ID()
            
        #check add_id against a list of known departments    
        elif not (var.dept_list).count(str(add_id)):
            msg_error("ID Set To:" + str(var.dept_alcohol_id) + "\n\n"
                      "You Have Entered an Invalid Department.")
            set_alcohol_ID()
            
        else:
            var.dept_alcohol_id.append(add_id)
            
            set_alcohol_ID()


#Set alcohol ID Checks    
def set_food_stamps():
    if not Path(var.dir_temp + "/" + var.plu_xml).is_file():
        msg_error("T13: Check Error\nFile Not Found. \n ")   
    else:
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root = tree.getroot()
        
        full_dept_list = []
        for dept in root.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            full_dept_list.append(sysid)
         
        #msg(var.dept_list)
            
        var.dept_food_stamps.sort()
        add_id = simpledialog.askinteger("Food Stamp Checks", 
             "ID Set To:" + str(var.dept_food_stamps) + "\n\n"
             "Enter '0' to End.\n"
             "What Department Would You Like to Add?")
           
        #0 Completes Input Process
        if add_id == 0:
            msg("Please Confirm: " + str(var.dept_food_stamps))
            for dept in var.dept_food_stamps:
                msg("Writing Food Stamp Checks to Department " + str(dept) + "\n"
                    "Please Be Patient.")
                write_flags(int(dept), 4)
                
            msg("Food Stamp Checks Have Been Added")
         
        #check add_id against the existing entries
        elif (var.dept_food_stamps).count(add_id):
            msg_error("ID Set To:" + str(var.dept_food_stamps) + "\n\n"
                      "Item Already On List")
            set_food_stamps()

        #check add_id against a list of known departments    
        elif not (var.dept_list).count(str(add_id)):
            msg_error("ID Set To:" + str(var.dept_food_stamps) + "\n\n"
                      "You Have Entered an Invalid Department.")
            set_food_stamps()
            
        else:
            var.dept_food_stamps.append(add_id)
            
            set_food_stamps()


'''            
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
''' 