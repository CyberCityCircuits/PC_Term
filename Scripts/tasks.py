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

from tkinter import *
from tkinter import messagebox, Label


#set varibles
export_complete = 1

    
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

        
def list_dept():
    
    #file_temp_merch = Path(dir_temp + "\\" + "poscfg.xml")
    if not Path(var.dir_temp + "/poscfg.xml").is_file():
        msg_error("T07: Check Error\n'poscfg.xml' Not Found. \n ")   
    else:
    
        #x = 0
        dept_list = []
        
        
        tree = et.parse(var.dir_temp + "//" + "poscfg.xml")
        root = tree.getroot()
        
        for dept in root.iter('department'):
            attributes = (dept.attrib)
            sysid = (attributes["sysid"])
            name = (attributes["name"])
            
            #print ((sysid.rjust(4)) + " - " + name.ljust(20))
            #sleep(.02)
            #x += 1
            #if x == (lines-7) or x == ((lines-7)*2) or x == ((lines-7)*3):
            dept = (sysid.rjust(4) + " " + name.ljust(20))
            dept_list.append(dept)
            #dept_list.append(name)
        
        
        dept_list_temp = dept_list
        #dept_list_len = len(dept_list)
        iterable = range(len(dept_list))
        
        
        dept_list_final = dept_list_temp
        
        x=0
        for item in iterable:
           x += 1
           if (x % 2 == 0): #even
               add_item = (dept_list.pop(0) + "    " + dept_list.pop(0))
               dept_list_final.append(add_item)       
        dept_list = '\n'.join(dept_list_final)
        #dept_list.insert(0, "List of Departments\n")
        msg(dept_list)
        
        #dept_list[0].grid(row=0, column=0)
        #dept_list[1].grid(row=0, column=1)
        #dept_list[2].grid(row=1, column=0)
        #dept_list[3].grid(row=1, column=1)
        
        #for r in range(3):
        #    for c in range(4):
        #        Label(root, text='R%s/C%s'%(r,c),
        #            borderwidth=1 ).grid(row=r,column=c)

                    

        
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
        msg("This Will Take Several Moments.\n\nPlease Be Patient.")
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
        if xmlin_dept.lstrip("0") == dept.lstrip("0"):
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

    msg(str(x) + " Food Stamp flags added to Department " + str(dept))
        
        
def write_id_chk(dept, value):
    x = 0
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
       
    if value == 1:
        idchk_value = ('domain:idCheck sysid="1"')
    elif value == 2:
        idchk_value = ('domain:idCheck sysid="2"')
    else:
        msg_error("There Was a Major Error.\n\nPlease Send The PC_Term_Report\nTo David Ray.")
        
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
        if xmlin_dept.lstrip("0") == dept.lstrip("0"):
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


        

