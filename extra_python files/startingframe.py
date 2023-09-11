from tkinter import *
import matplotlib
import os
from pandas import DataFrame
import numpy as np
import pandas as pd
from tkinter import ttk
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from Functions import *
from tkinter import filedialog
from tkinter import colorchooser
matplotlib.use('TkAgg')

from tkinter import messagebox
from custom_widget import *
from boxplotV2 import BoxPlotV2

class StartingFrame(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ##Box frame
        self.box = Frame(self, bg='white', relief='solid', borderwidth=0)
        self.box.place(relx=0, rely=0, relwidth=1, relheight=1)

        #listbox
        lable1 = Label(self.box, text='All Batches', font='calibri 14', bg='white')
        lable1.place(x=47, y=10)
        self.lb_1 = Listbox(self.box, bg='white', relief='solid', borderwidth=1, selectmode ='extended', exportselection = FALSE)
        self.lb_1.place(x=50, y= 50)
        self.main_folder_dir = os.getcwd() + '/Batches'

        elements_of_main_folder_keys = [i for i  in os.listdir(self.main_folder_dir) if os.path.isdir(self.main_folder_dir+'/'+i)]
        elements_of_main_folder_values = [self.main_folder_dir + '/' + i for i in elements_of_main_folder_keys ]

        self.elements_of_main_folder = zip(elements_of_main_folder_keys, elements_of_main_folder_values)
        self.elements_of_main_folder = dict(self.elements_of_main_folder)



        for i in list(self.elements_of_main_folder.keys()):
            self.lb_1.insert(list(self.elements_of_main_folder.keys()).index(i), i)


        self.lb_1.bind('<<ListboxSelect>>', self.items_selected)

        #second list box
        lable2 = Label(self.box, text='Splits', font='calibri 14', bg='white')
        lable2.place(x=272, y=10)

        self.lb_2 = Listbox(self.box, bg='white', relief='solid', borderwidth=1,selectmode ='extended', exportselection = FALSE)
        self.lb_2.place(x=272, y=50)
        self.lb_2.bind('<<ListboxSelect>>', self.items_selected_2)

        lable3 = Label(self.box, text = 'Batch Details:',font='calibri 14', bg = 'white')
        lable3.place(x=495,y =10)
        self.save_button = CustomButton(self.box, text='Update Batch Details', command = self.save_batch_details)
        self.save_button.place(x=498, y=560)

        self.batch_details = Text(self.box, bg='white', relief='solid', borderwidth=1)
        self.batch_details.place(x=500, y=50, width=400, height=500)

        Button(self.box, text='Plot',command = self.plot, font='calibri 18', borderwidth=0,
               fg='white',
               bg='#28486B', cursor="hand2").place(x=80, y=310, width = 300)

        ##few global variables
        self.split_count = 0
        self.entry_list = []  ##to store all the string variables of entry widget
        self.entry_widget_list = []  ## storing all the entry widget
        self.DF = pd.DataFrame()
        self.selected_split_values = []


    def items_selected(self, event):
        """ handle item selected event
        """
        # get selected indices
        self.lb_2.delete(0, 'end')
        self.batch_details.delete(0.0,END)
        selected_indices = self.lb_1.curselection()
        # get selected items
        selected_elements_keys = [self.lb_1.get(i) for i in selected_indices]
        selected_elements_values = [self.elements_of_main_folder[i] for i in selected_elements_keys]
        selected_elements = zip(selected_elements_keys,selected_elements_values)
        selected_elements = dict(selected_elements)


        elements_of_selected_elements_keys =[]
        elements_of_selected_elements_values = []
        for i in list(selected_elements.values()):
            all_dirs_in_main_dir = os.listdir(i) #os.listdir only return the end name and hence to get complete directory we need to add the prevoious adress
            all_dirs_in_main_dir_keys = [x for x in all_dirs_in_main_dir if os.path.isdir(i+'/'+x)]
            all_dirs_in_main_dir_values = [i + '/' + x for x in all_dirs_in_main_dir_keys]
            for dir in all_dirs_in_main_dir_values:
                elements_of_selected_elements_values.append(dir)
            for dir in all_dirs_in_main_dir_keys:
                elements_of_selected_elements_keys.append(dir)
                self.lb_2.insert(all_dirs_in_main_dir_keys.index(dir), dir)

        elements_of_selected_elements = zip(elements_of_selected_elements_keys,elements_of_selected_elements_values)
        self.elements_of_selected_elements = dict(elements_of_selected_elements)



        batch_address = selected_elements_values[0]
        self.file_address_of_selected_batch = batch_address + '/details.txt'

        if os.path.isfile(self.file_address_of_selected_batch):
            with open(self.file_address_of_selected_batch, 'r') as file:
                self.batch_details.insert(INSERT, file.read())



        else:
            file = open(self.file_address_of_selected_batch, 'w')

    def items_selected_2(self, event):

        """ handle item selected event
               """
        # get selected indices

        selected_indices = self.lb_2.curselection()
        # get selected items
        self.selected_splits_keys = [self.lb_2.get(i) for i in selected_indices]
        self.selected_split_values = [self.elements_of_selected_elements[i] for i in self.selected_splits_keys]


    def save_batch_details(self):
        data = self.batch_details.get(0.0, END)
        with open(self.file_address_of_selected_batch, 'w') as file:
            file.write(data)

        messagebox.showinfo(title = 'Sucess',message = 'Details Updated')



    def plot(self):
        if self.selected_split_values == []:
            messagebox.showinfo(title='Error', message='No Splits Selected')
        else:
            new_window = BoxPlotV2(address=self.selected_split_values)
            new_window.mainloop()
















