# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 22:10:13 2017

@author: admin
"""
import  var

import os
from bs4 import BeautifulSoup as bs
import lxml.etree as et


#Removed all Food Stamp Tags.  Verified Working.    
def remove_fs():
    x = 0
    tasks.chk_file_temp("PLUs.xml")
    set_date_time()
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
    f.write("Remove Food Stamp Flags " + currdate + " " + currtime + "\n")
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
    
        
#set date and time        
def set_date_time():
    global currdate, currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")
        


    