from boxplot import DataPlot
from tkinter import Scrollbar
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import os
from Functions import *
from custom_widget import *

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)


current_user = ''
current_user_dir = os.getcwd()
# current_user = 'Rahul Patidar'
# current_user_dir = 'C:/Users/pcgre/OneDrive - Swansea University/Projects/Python/PlotIT_latest/users/Rahul Patidar'
user_folder = current_user_dir + '/users'
if not os.path.exists(user_folder):
    os.makedirs(user_folder)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PlotIT 3.0')
        self.iconbitmap(r'icon.ico')
        self.configure(background='white')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(0.8 * screen_width)
        height = int(0.7 * screen_height)
        self.geometry(f'{width}x{height}+100+100')
        self.minsize(1300, 750)

        # Container frame to contain all the other frames
        container = tk.Frame(self, bg='white')
        container.place(relx=0, rely=0, relwidth=1, relheight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Frame 1
        side_column = tk.Frame(container, borderwidth=0,
                               relief=tk.RIDGE, bg='#28486B')
        side_column.place(relx=0, rely=0, width=300, relheight=1)

        open_image = Image.open('specific.png')
        open_image = open_image.resize((250, 100), Image.LANCZOS)
        img = ImageTk.PhotoImage(open_image)
        image_label = tk.Label(side_column, image=img, borderwidth=0)
        image_label.place(relx=0.08, rely=0.85)
        image_label.image = img

        self.frames = {}
        for F in [MainData, JVMeasurement, ExperimentPlanner]:
            frame = F(container, self)
            self.frames[F] = frame
            frame.config(bg='white', borderwidth=1)
            frame.place(x=300, rely=0, relwidth=1, relheight=1)

        user_icon_open = Image.open('usericon.png')
        user_icon = ImageTk.PhotoImage(user_icon_open)
        user_icon_label = tk.Label(side_column, image=user_icon, borderwidth=0)
        user_icon_label.place(x=20, y=50)
        user_icon_label.image = user_icon

        self.user_label = tk.Label(side_column, text=current_user, font='calibri 20', fg='white',
                                   bg='#28486B')
        self.user_label.place(x=70, y=47)
        #
        # tk.Button(side_column, command=lambda: self.show_frame(BoxPlot), text='BoxPlot', font='calibri 18',
        #           borderwidth=0,
        #           fg='white',
        #           bg='#28486B', cursor="hand2").place(x=20, y=150)
        # tk.Button(side_column, command=lambda: self.show_frame(JV), text='JV', font='calibri 18', borderwidth=0,
        #           fg='white',
        #           bg='#28486B', cursor="hand2").place(x=20, y=220)
        # tk.Button(side_column, command=lambda: self.show_frame(EQE), text='EQE', font='calibri 18', borderwidth=0,
        #           fg='white',
        #           bg='#28486B', cursor="hand2").place(x=20, y=310)
        # tk.Button(side_column,command=self.readme, text='Help', font=('calibri 15'), borderwidth=0, fg='white',
        #    bg='#28486B', cursor="hand2").place(x=20, y=390)
        tk.Button(side_column, command=lambda: self.show_frame(MainData), text='Data Plotting', font=('calibri 18'),
                  borderwidth=0, fg='white',
                  bg='#28486B', cursor="hand2").place(x=30, y=150)

        tk.Button(side_column, command=lambda: self.show_frame(ExperimentPlanner), text='Experiment Planner', font='calibri 18', borderwidth=0,
                  fg='white',
                  bg='#28486B', cursor="hand2").place(x=30, y=210)
        tk.Button(side_column, command=lambda: self.show_frame(JVMeasurement), text='JV Measurement', font='calibri 18',
                  borderwidth=0,
                  fg='white',
                  bg='#28486B', cursor="hand2").place(x=30, y=270)

    def readme(self):
        top = tk.Toplevel()
        top.wm_geometry('800x400')
        text = '\nPlease follow the following steps to plot your data:\n\nStep 1: Organize the files in individual folders that you would like to plot.\n              For example, file of devices annealed at 100C in one folder, 150C in other folder and so on so forth. ' \
               '\n\nStep 2: Select these folders one by one by clicking on select split button.\n\nSplit count will give you the number of splits you have selected.\n\n\nThats all, you can now choose the options you would like to plot.\n\nIn case if you face any problem or the software crashes, let me know.\n\nHappy Plotting!\n\nRahul Patidar\nrahul.patidar@swansea.ac.uk'
        label = tk.Label(top, text=text, font=('arial 12'), justify=tk.LEFT)
        label.pack(side=tk.LEFT)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class ExperimentPlanner(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)


class JVMeasurement(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)


class EQE(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)


class PL(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)


class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('700x400')
        self.configure(bg='white')
        self.title('Plot IT')
        self.iconbitmap(r'icon.ico')

        label = tk.Label(self, text='Select User', bg='white',
                         fg='#28486B', font='calibri 16').place(x=90, y=46)
        self.user_var = tk.StringVar(self)

        self.user_list = os.listdir(os.getcwd() + '/users')
        self.select_user = ttk.Combobox(self, font='calibri 14', width=20, textvariable=self.user_var,
                                        values=self.user_list, postcommand=lambda: self.select_user.configure(
                                            values=self.user_list), state='readonly')
        self.select_user.place(x=250, y=50)

        CustomButton(self, text='Log In', font='calibri 14', fg='#28486B', width=33, command=lambda: self.login()).place(
            x=102, y=150)

        tk.Button(self, text='New User', bg='white', fg='#28486B', font='calibri 14', borderwidth=0, cursor='hand2',
                  command=lambda: self.new_user()).place(x=250, y=300)

    def login(self):
        if self.user_var.get() != '':
            self.destroy()
            global current_user
            current_user = self.user_var.get()
            global current_user_dir
            current_user_dir = current_user_dir + '/users/' + f'{current_user}'
        else:
            messagebox.showinfo(
                title='Error!', message='Please fill in the required details')

    def new_user(self):
        self.new_window = tk.Tk()
        self.new_window.title('New User Registration')
        self.new_window.iconbitmap(r'icon.ico')
        self.new_window.geometry('500x300')
        self.new_window.configure(bg='white')
        label = tk.Label(self.new_window, text='Name', bg='white',
                         fg='#28486B', font='calibri 14').place(x=30, y=20)
        self.name_entry_variable = tk.StringVar(self.new_window)
        name_entry = CustomEntry(self.new_window, textvariable=self.name_entry_variable, width=20,
                                 font='calibri 14').place(x=150, y=24)

        # label = tk.Label(self.new_window, text='Group', bg='white', fg='#28486B', font='calibri 14').place(x=30, y=70)
        #
        # self.group_variable = tk.StringVar(self.new_window)
        # group = ttk.Combobox(self.new_window, textvariable=self.group_variable, font='calibri 14',
        #                      values=['R2R', 'Carbon', 'OPV'], state='readonly', width=18).place(x=150, y=74)

        tk.Button(self.new_window, text='Register', fg='white', bg='#28486B', width=20, font='calibri 12',
                  command=lambda: self.add_new_user()).place(x=130, y=150)
        self.new_window.mainloop()

    def add_new_user(self):

        if self.name_entry_variable.get() != '':
            new_user_dir = os.getcwd() + \
                f'/users/{self.name_entry_variable.get()}'
            if not os.path.exists(new_user_dir):
                os.makedirs(new_user_dir)

                self.user_list.append(f'{self.name_entry_variable.get()}')
                messagebox.showinfo(message='Done')
                self.new_window.destroy()
            else:

                messagebox.showinfo(message='User already exists.')
                self.new_window.deiconify()  # bring the current window on top

        else:

            messagebox.showinfo(
                title='Error!', message='Please fill in the details')
            self.new_window.deiconify()  # bring the current window on top


class MainData(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Box frame
        self.box = tk.Frame(self, bg='white', relief='solid', borderwidth=0)
        self.box.place(relx=0, rely=0, relwidth=1, relheight=1)

        # listbox
        label1 = tk.Label(self.box, text='All Batches',
                          font='calibri 14', bg='white')
        label1.place(x=47, y=10)
        self.lb_1 = tk.Listbox(self.box, bg='white', relief='solid', borderwidth=1, selectmode='extended',
                               exportselection=False)
        self.lb_1.place(x=50, y=50)
        self.main_folder_dir = current_user_dir

        elements_of_main_folder_keys = [i for i in os.listdir(self.main_folder_dir) if
                                        os.path.isdir(self.main_folder_dir + '/' + i)]
        elements_of_main_folder_values = [
            self.main_folder_dir + '/' + i for i in elements_of_main_folder_keys]

        self.elements_of_main_folder = dict(
            zip(elements_of_main_folder_keys, elements_of_main_folder_values))

        for i in self.elements_of_main_folder.keys():
            self.lb_1.insert(
                list(self.elements_of_main_folder.keys()).index(i), i)

        self.lb_1.bind('<<ListboxSelect>>', self.items_selected)

        # second list box
        label2 = tk.Label(self.box, text='Splits',
                          font='calibri 14', bg='white')
        label2.place(x=272, y=10)

        self.lb_2 = tk.Listbox(self.box, bg='white', relief='solid', borderwidth=1, selectmode='extended',
                               exportselection=False)
        self.lb_2.place(x=272, y=50)
        self.lb_2.bind('<<ListboxSelect>>', self.items_selected_2)

        label3 = tk.Label(self.box, text='Batch Details:',
                          font='calibri 14', bg='white')
        label3.place(x=495, y=10)
        self.save_button = CustomButton(
            self.box, text='Update Batch Details', command=self.save_batch_details)
        self.save_button.place(x=498, y=560)

        self.batch_details = tk.Text(
            self.box, bg='white', relief='solid', borderwidth=1)
        self.batch_details.place(x=500, y=50, width=400, height=500)

        tk.Button(self.box, text='Plot', command=self.plotit, font='calibri 18', borderwidth=0,
                  fg='white',
                  bg='#28486B', cursor="hand2").place(x=80, y=330, width=300)

        # Scrollbar
        scrollbar = Scrollbar(self.box)
        scrollbar.place(x=910, y=50, relheight=0.92)
        self.batch_details = tk.Text(
            self.box, bg='white', relief='solid', borderwidth=1, yscrollcommand=scrollbar.set)
        self.batch_details.place(x=500, y=50, width=400, height=500)
        scrollbar.config(command=self.batch_details.yview)

        # Few global variables
        self.split_count = 0
        self.entry_list = []  # To store all the string variables of entry widget
        self.entry_widget_list = []  # Storing all the entry widget
        self.DF = pd.DataFrame()
        self.selected_split_values = []

    def items_selected(self, event):
        # Handle item selected event
        self.lb_2.delete(0, 'end')
        self.batch_details.delete(0.0, tk.END)
        selected_indices = self.lb_1.curselection()
        selected_elements_keys = [self.lb_1.get(i) for i in selected_indices]
        selected_elements_values = [
            self.elements_of_main_folder[i] for i in selected_elements_keys]
        self.elements_of_selected_elements = {}

        for value in selected_elements_values:
            dirs = [dir for dir in os.listdir(
                value) if os.path.isdir(os.path.join(value, dir))]
            for dir in dirs:
                self.elements_of_selected_elements[dir] = os.path.join(
                    value, dir)
                self.lb_2.insert(tk.END, dir)

        batch_address = selected_elements_values[0]
        self.file_address_of_selected_batch = os.path.join(
            batch_address, 'details.txt')

        if os.path.isfile(self.file_address_of_selected_batch):
            with open(self.file_address_of_selected_batch, 'r') as file:
                self.batch_details.insert(tk.INSERT, file.read())
        else:
            file = open(self.file_address_of_selected_batch, 'w')

    def items_selected_2(self, event):
        selected_indices = self.lb_2.curselection()
        self.selected_splits_keys = [
            self.lb_2.get(i) for i in selected_indices]
        self.selected_split_values = [
            self.elements_of_selected_elements[i] for i in self.selected_splits_keys]

    def save_batch_details(self):
        data = self.batch_details.get(0.0, tk.END)
        with open(self.file_address_of_selected_batch, 'w') as file:
            file.write(data)
        messagebox.showinfo(title='Success', message='Details Updated')

    def plotit(self):
        if not self.selected_split_values:
            messagebox.showinfo(title='Error', message='No Splits Selected')
        else:
            new_window_app = DataPlot(address=self.selected_split_values)
            new_window_app.mainloop()


login = LoginWindow()
login.mainloop()


def on_closing():
    # Destroy the window
    app.destroy()


if current_user != '':
    app = App()
    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
else:
    login.quit()
