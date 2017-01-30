# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 13:23:32 2016

@author: David A Ray - CBE Inc.
"""

#import libraries
import os
import re
import datetime as dt
import shutil
import xml.etree.ElementTree as et

#set varibles
dir_fresh = ('Put_PLUs_Here')
dir_clean = ('Cleaned_PLUs')
dir_dirty = ('Dirty_PLUs')
dir_temp = ('Temp_PLUs')
file_plu = ('PLUs.XML')
file_plu_bu = ('PLUs_BackUp.XML')
file_plu_temp = ('PLUs_Temp.XML')
regex = re.compile(r'<pcode>(.*)</pcode>')
value = '<pcode>0</pcode>'

#################################################
#MAIN MENU
def logo():
    print ("------------------")
    print ("")
    print ("")
    print ("")
    print ("")
    print ("")    
    print (" _______                            __                        __             ______                   __           ")
    print ("/       \                          /  |                      /  |           /      \                 /  |          ")
    print ("$$$$$$$  | ______    ______    ____$$ | __    __   _______  _$$ |_         /$$$$$$  |  ______    ____$$ |  ______  ")
    print ("$$ |__$$ |/      \  /      \  /    $$ |/  |  /  | /       |/ $$   |        $$ |  $$/  /      \  /    $$ | /      \ ")
    print ("$$    $$//$$$$$$  |/$$$$$$  |/$$$$$$$ |$$ |  $$ |/$$$$$$$/ $$$$$$/         $$ |      /$$$$$$  |/$$$$$$$ |/$$$$$$  |")
    print ("$$$$$$$/ $$ |  $$/ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |        $$ | __       $$ |   __ $$ |  $$ |$$ |  $$ |$$    $$ |")
    print ("$$ |     $$ |      $$ \__$$ |$$ \__$$ |$$ \__$$ |$$ \_____   $$ |/  |      $$ \__/  |$$ \__$$ |$$ \__$$ |$$$$$$$$/ ")
    print ("$$ |     $$ |      $$    $$/ $$    $$ |$$    $$/ $$       |  $$  $$/       $$    $$/ $$    $$/ $$    $$ |$$       |")
    print ("$$/      $$/        $$$$$$/   $$$$$$$/  $$$$$$/   $$$$$$$/    $$$$/         $$$$$$/   $$$$$$/   $$$$$$$/  $$$$$$$/ ")
    print ("")
    print ("")
    print (" ________                                 __                        __                                             ")
    print ("/        |                               /  |                      /  |                                            ")
    print ("$$$$$$$$/______    ______   _____  ____  $$/  _______    ______   _$$ |_     ______    ______                      ")
    print ("   $$ | /      \  /      \ /     \/    \ /  |/       \  /      \ / $$   |   /      \  /      \                     ")
    print ("   $$ |/$$$$$$  |/$$$$$$  |$$$$$$ $$$$  |$$ |$$$$$$$  | $$$$$$  |$$$$$$/   /$$$$$$  |/$$$$$$  |                    ")
    print ("   $$ |$$    $$ |$$ |  $$/ $$ | $$ | $$ |$$ |$$ |  $$ | /    $$ |  $$ | __ $$ |  $$ |$$ |  $$/                     ")
    print ("   $$ |$$$$$$$$/ $$ |      $$ | $$ | $$ |$$ |$$ |  $$ |/$$$$$$$ |  $$ |/  |$$ \__$$ |$$ |                          ")
    print ("   $$ |$$       |$$ |      $$ | $$ | $$ |$$ |$$ |  $$ |$$    $$ |  $$  $$/ $$    $$/ $$ |                          ")
    print ("   $$/  $$$$$$$/ $$/       $$/  $$/  $$/ $$/ $$/   $$/  $$$$$$$/    $$$$/   $$$$$$/  $$/                           ")
    print ("")
    print ("    Version 0.3")
    print ("    David A Ray")


def main_menu():
    print ("")
    logo()
    print ("")
    print ("")
    confirm = raw_input("You want to remove Product Codes? (Y/N)")
    if confirm == 'y' or confirm == 'Y':
        print ("The existing PLU file is being backed up to a folder called Dirty_PLUs")
    else:
        return main_menu()

#################################################

def setcurrdate():
    global currdate
    currdate = dt.date.today().strftime("%Y%m%d")

def setcurrtime():
    global currtime
    currtime = dt.datetime.now().strftime("%H%M%S")


#################################################
#CLEANING PLUS

def copy_plu():
    shutil.copy2(dir_fresh + "/" + file_plu, dir_fresh + "/" + file_plu_temp)
    os.rename(dir_fresh + "/" + file_plu_temp, file_plu)
    
def put_plu():
    os.remove(dir_fresh + "/" + file_plu)
    os.rename(file_plu, dir_fresh + "/" + file_plu)

#create directory for old plu file
def backup_plu():
    global dir_dirty
    global file_plu
    global file_plu_bu
    global currdate
    global currtime
    dir_bu = (dir_dirty + "-" + currdate + "-" + currtime)
    if not os.path.exists(dir_bu):
        os.makedirs(dir_bu)
    os.system ("copy %s %s" % (file_plu, file_plu_bu))
    os.rename(file_plu_bu, dir_bu + "/" + file_plu)

'''From V0.2
def read(file_plu):
    with open(file_plu, 'r') as file:
        #read the file
        data = file.read()
        #return
        return data

def process(file_plu, data):
    with open(file_plu, 'w') as file:
        #search the data for the pattern and replace with the new value
        output = re.sub(regex, value, data)
        #write the data to the file passed
        file.write(output)
'''

#New XML Script From T Silvestru
def process2():
    tree = et.parse('PLUs.xml')
    root = tree.getroot()
    for pcode in root.iter('pcode'):
        pcode.text = str(0)
    tree.write(file_plu)

##################################################

#Run Commands
if __name__ == "__main__":
    main_menu()
    setcurrdate()
    setcurrtime()
    copy_plu()
    backup_plu()
    process2()
    put_plu()