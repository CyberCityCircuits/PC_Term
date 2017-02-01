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
version = "0.06.00G"
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
dept_alcohol_id = []
full_dept_list = []

#define system varibles
wait = 3.0
width = 60
lines = 35
cent_width = int(width)-1

currdate = dt.date.today().strftime("%Y%m%d")
currtime = dt.datetime.now().strftime("%H%M%S")

x = 0

def header():
    print("Food Stamp Test")

#checks if file exists in dir_temp
def chk_file_temp(file_name):
    if not Path(dir_temp + "/" + file_name).is_file():
        header()
        print ()
        print ("FILE NOT FOUND".center(cent_width))
        os.system("pause")
        
        
        
        
def reset_fs():
    global export_complete

    infile  = os.path.abspath(dir_temp + "/" + plu_xml)
    outfile = os.path.abspath(dir_temp + "/" + plu_xml_2)
    
    export_complete = 0    
    chk_file_temp("PLUs.xml")    
    x = 0
    file_fschk = (dir_temp + "/" + plu_xml)
    
    tree = et.parse(file_fschk)
    root = tree.getroot()
    fs_count = (0)
    
    with open(infile) as xmlin:
        soup = bs(xmlin, 'xml')

    header()
    print ("Processing...".center(cent_width))
    for c in root:
        
        x += 1
        #print (("Checking... " + (str(x).rjust(5))).center(cent_width))

        #THIS IS BAD.  IT REMOVES ALL FLAGS, NOT JUST FOOD STAMPS
        for tag in soup('flags'):
            #tag.decompose()
            flag_tag = tag.children
            
            print (flag_tag)
            

    with open(outfile, 'w') as xmlout:
        xmlout.write(soup.prettify())
        
    xmlout.close()
          
    
    header()
    print ()
    print (("Food Stamped Items: " + str(fs_count).rjust(5)).center(cent_width))
    print ()
    print (("PLUs Checked: " + str(x).rjust(5)).center(cent_width))
    print ()
    print ("All Food Stamped Checks will be removed.".center(cent_width))
    print ()
    print ("Please wait while your file is being processed.".center(cent_width))

    sleep(2)





reset_fs()
        