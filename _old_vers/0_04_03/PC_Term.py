# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 13:23:32 2016

@author: David A Ray - CBE Inc.
"""

#V0_01 - import libraries
import os
import re
import datetime as dt
import shutil
#import xml.etree.ElementTree as et
import lxml.etree as et
#import codecs
from time import sleep

#V0_04_03 - Set console size and color
os.system("mode con: cols=50 lines=25")
os.system('color F')

#V0_01 - set varibles
dir_fresh = ('Put_PLUs_Here')
dir_clean = ('Cleaned_PLUs')
dir_dirty = ('Dirty_PLUs')
dir_temp = ('Temp_PLUs')
file_plu = ('PLUs.XML')
file_plu2 = ('PLUs2.XML')
file_plu_bu = ('PLUs_BackUp.XML')
file_plu_temp = ('PLUs_Temp.XML')
count = 0
regex = re.compile(r'<pcode>(.*)</pcode>')
value = '<pcode>0</pcode>'

#################################################
#V0_01 - MAIN MENU
def logo():  
    os.system('cls')
    os.system('echo off')
    print ("    -----------------------------------------")
    print ("             _______          ______ ")
    print ("            /       \        /      \.")
    print ("            $$$$$$$  |      /$$$$$$  |")
    print ("            $$ |__$$ |      $$ |  $$/")
    print ("            $$    $$/       $$ |")
    print ("            $$$$$$$/        $$ |   __")
    print ("            $$ |            $$ \__/  |")
    print ("            $$ |            $$    $$/")
    print ("            $$/              $$$$$$/")
    print ("     ________")   
    print ("    /        |")    
    print ("    $$$$$$$$/______    ______   _____  ____")
    print ("       $$ | /      \  /      \ /     \/    \ ")
    print ("       $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |")
    print ("       $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |")
    print ("       $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |")
    print ("       $$ |$$       |$$ |      $$ | $$ | $$ |")
    print ("       $$/  $$$$$$$/ $$/       $$/  $$/  $$/ ")
    print ("    -----------------------------------------")
    print ("        Product Code Terminator V 0.04.03")    
    print ("                   David A Ray")
    print ("")
    print ("     The existing PLU file is being backed up")
    print ("         to a folder called \"Dirty PLUs\".")
def main_menu():
    print ("")
    logo()
'''    
    print ("")
    confirm = raw_input("     You want to remove Product Codes? (Y/N)")
    if confirm == 'y' or confirm == 'Y':
        print ("The existing PLU file is being backed up to a folder called Dirty_PLUs")
    else:
        return main_menu()
'''

#################################################
#V0_01 - SET DATE AND TIME (Update V0_04_02)
def setcurrdt():
    global currdate
    global currtime
    currdate = dt.date.today().strftime("%Y%m%d")
    currtime = dt.datetime.now().strftime("%H%M%S")
    
#################################################
#CLEANING PLUS
#V0_01 - COPY PLU TO WORKING DIR
def copy_plu():
    shutil.copyfile(dir_fresh + "/" + file_plu, file_plu)

  
#V0_04 - PUT CLEAN PLU IN dir_clean
def put_plu():
    dir_put = (dir_clean + "-" + currdate + "-" + currtime)
    if not os.path.exists(dir_put):
        os.makedirs(dir_put)    
    shutil.copyfile(file_plu, dir_put + "/" + file_plu)
    
#V0_01 - create and move plu file to directory for back up plu file
def backup_plu():
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    if not os.path.exists(dir_bu):
        os.makedirs(dir_bu)
    shutil.copyfile(file_plu, dir_bu + "/" + file_plu)
    
#V0_04 - DELETE FILE WE WERE WORKING WITH
def delete_plu():
    os.remove(file_plu)    

'''    
#V0_02 - Trying to edit it as a text file.
def read02():
    with open(file_plu, 'r') as file:
        global data
        #read the file
        data = file.read()
        #return
        return data

def process02():
    with open(file_plu, 'w') as file:
        #search the data for the pattern and replace with the new value
        output = re.sub(regex, value, data)
        #write the data to the file passed
        file.write(output)
'''
'''
#V0_03 - New XML Script From T Silvestru
def process03():
        tree = et.parse('PLUs.xml')
        root = tree.getroot()
        for pcode in root.iter('pcode'):
            pcode.text = str(0)
        tree.write(file_plu)
'''
'''
#V0_04_01 - New Script from PyNight - Cory Taylor
def process04():
    with codecs.open(file_plu, 'r', 'utf-8') as f:
            tree = et.parse(f)
            root = tree.getroot()
            outfile = codecs.open(file_plu2, 'w', 'utf-8')

            newxml = et.ElementTree()
            newxml.iter
            
            
            for pcode in root.iter('pcode'):
                pcode.text = str(0)
            et.ElementTree(tree).write(outfile, encoding = 'UTF-8', xml_declaration = True)
'''
'''
#V0_04_02 - New Script Using For Loops            
def process05():
    with open (file_plu) as f:    
        data = f.readlines() #puts all lines of PLU file in a list of strings
    for line in data:
        #split_data = line.split()
        #tag = split_data[0].strip()  
        #if tag[0] == ('<PLU'):
        #    print tag[0]
        #if line.startswith(<PLU) == TRUE:
        print (line)
'''

#V0_04_03 = Derivations of process03
def process06():
    tree = et.parse(file_plu)
    root = tree.getroot()
    for pcode in root.iter('pcode'):
        pcode.text = str(0)
    tree.write(file_plu,encoding="UTF-8",xml_declaration=True)
        
##################################################

#V0_01 - Run Commands
if __name__ == "__main__":
    main_menu() #Comment out for faster testing.
    sleep(3)
    setcurrdt()
    copy_plu()
    backup_plu()
    process06()
    put_plu()
    delete_plu()