# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:24:54 2017

@author: admin
"""
import tasks, PC_Term, process, var

from tkinter import *
from tkinter import messagebox

app_name = PC_Term.long_app
version = PC_Term.version


class Window(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title(app_name)
        self.pack(fill=BOTH, expand=1)
        
        #exit_button = Button(self, text = "Exit", command=exit)
        #exit_button.place(x = 170, y = 270)
        
        topbar = Menu(self.master)
        self.master.config(menu=topbar)
        
        file = Menu(topbar)
        edit = Menu(topbar)
        remove = Menu(topbar)
        add = Menu(topbar)
        help_menu = Menu(topbar)
        
        file.add_command(label="Import Dataset")
        file.add_command(label="Export Dataset")
        file.add_command(label="Exit", command=self.client_exit)
        topbar.add_cascade(label="File", menu=file)
        
        
        #edit.add_command(label="Remove Product Codes")
        #edit.add_command(label="Remove ID Checks")
        #edit.add_command(label="Remove Food Stamp Checks")
        #edit.add_command(label="Set ID Checks by Department")
        #edit.add_command(label="Set Food Stamp Checks by Department")
        #topbar.add_cascade(label="Edit", menu=edit)
        

        remove.add_command(label="Remove Product Codes")
        remove.add_command(label="Remove ID Checks")
        remove.add_command(label="Remove Food Stamp Checks")

        topbar.add_cascade(label="Remove", menu=remove)

        add.add_command(label="Set ID Checks by Department")
        add.add_command(label="Set Food Stamp Checks by Department")


        
    
        topbar.add_cascade(label="Add", menu=add)
        
        
        
        
        topbar.add_cascade(label="Help", menu=help_menu)
        
        
        
        
        
        
    def client_exit(self):
        exit()
        
def msg(text):
    messagebox.showinfo(app_name, text)
    

        

root = Tk()
root.geometry("400x300")

app = Window(root)    

root.mainloop()

