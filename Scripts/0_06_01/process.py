# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:10:13 2017

@author: admin
"""
import tasks, PC_Term, var

import os
from bs4 import BeautifulSoup as bs
import lxml.etree as et

cent_width = PC_Term.cent_width

#Removed all Food Stamp Tags.  Verified Working.    
def remove_fs():
    x = 0
    tasks.chk_file_temp("PLUs.xml")
    tasks.set_date_time()
    PC_Term.header()
    print ("Processing...".center(cent_width))
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
    f.write("Remove Food Stamp Flags " + tasks.currdate + " " + tasks.currtime + "\n")
    f.write("Removed Flag Count " + str(x) + "\n")
    f.write("\n")
    f.close()   

    
    PC_Term.header()
    print ("All Food Stamp Tags Removed".center(cent_width))
    print (("Removed " + str(x) + " Food Stamp Tags").center(cent_width))
    tasks.sleep(3)

    
#remove all product codes
def remove_pcode():
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
        print (("Checking... " + (str(x).rjust(5))).center(cent_width))
        #tasks.pause(.00001)
    print ("  Processing...")
    tasks.pause(2)
    
def write_id_chk(dept, value):
    x = 0
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
       
    if value == 1:
        idchk_value = ('domain:idCheck sysid="1"')
    elif value == 2:
        idchk_value = ('domain:idCheck sysid="2"')
    else:
        PC_Term.header()
        print ("There was a major error.".center(cent_width))
        print ("Please send the PC_Term_Report to David Ray.".center(cent_width))
        
        tasks.set_date_time()
        
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Error writing ID checks. " + tasks.currdate + " " + tasks.currtime + "\n")
        
        f.write("Location - process_write_id_chk\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
        print()
        print()
        print()
        tasks.pause(0)
        PC_Term.main_menu()
        
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

    tasks.set_date_time()
    
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Writing ID Checks " + tasks.currdate + " " + tasks.currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    
    print ("  " + str(x) + " ID Checks added to Department " + str(dept))
    
def write_flags(dept, value):
    infile  = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    outfile = os.path.abspath(var.dir_temp + "/" + var.plu_xml)
    
    tasks.set_date_time()
    
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
        PC_Term.header()
        print ("There was a major error.".center(cent_width))
        print ("Please send the PC_Term_Report to David Ray.".center(cent_width))
        
        tasks.set_date_time()
        
        f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
        f.write("Error writing flags. " + tasks.currdate + " " + tasks.currtime + "\n")
        f.write("Location - process_write_flags\n")
        f.write("Department - " + str(dept) + "\n")
        f.write("Value - " + str(value) + "\n")
        f.write("\n")
        f.close()   
        print()
        print()
        print()
        tasks.pause(0)
        PC_Term.main_menu()

    
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
    
    
    f = open(var.dir_temp + "\\" + var.log_name + ".txt","a")
    f.write("Writing Food Stamps " + tasks.currdate + " " + tasks.currtime + "\n")
    f.write("Department - " + str(dept) + "\n")
    f.write("Value - " + str(value) + "\n")
    f.write("Amount Added - " + str(x) + "\n")
    f.write("\n")
    f.close()   

    print ("  " + str(x) + " Food Stamp flags added to Department " + str(dept))
    
    tasks.pause(2)
    

    