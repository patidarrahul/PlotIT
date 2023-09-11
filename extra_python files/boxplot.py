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
class BoxPlot(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ##figure frame
        self.box_plot = Frame(self, bg='white', relief='solid', borderwidth=0)
        self.box_plot.place(relx=0, rely=0, relwidth=1, relheight=0.75)

        ##customize_column
        customize = Frame(self, bg='white', relief='solid', borderwidth=1)
        customize.place(relx=0, rely=0.75, relwidth=1, relheight=1)
        label_customize = Label(self, text='Customize', bg='white', font='Calibri 14')
        label_customize.place(x=50, rely=0.72, relheight=0.06)

        Button(self.box_plot, text='Select Data', font='calibri 14', command=self.dataframe_creation, borderwidth=0,
               bg='white', cursor='hand2').place(x=3, y=0)

        Label(customize, text='Scan:', font=('calibri 13'), bg='white', fg='#28486B').place(x=14, y=30)
        self.scan_choice = ['Reverse', 'Forward', 'Together']
        self.scan_choice_var = StringVar()
        self.scan_choice_var.set('Reverse')
        menu_2 = ttk.Combobox(customize, textvariable=self.scan_choice_var, values=self.scan_choice, state='readonly')
        menu_2.place(x=100, y=34)
        menu_2.config(font=('calibri', (10)), width=8)
        self.split_count = 0

        self.optionlist = {'PCE': 'Power Conversion Efficiency (%)', 'Jsc': 'Current Density (mA/cm$^2$)',
                           'FF': 'Fill Factor (%)', 'Voc': 'Open Circuit Voltage (Volts)'}
        Label(customize, text='Y-axis:', font=('calibri 12'), bg='white', fg='#28486B').place(x=14, y=74)
        global parameter
        parameter = StringVar()

        parameter.set('PCE')
        menu = ttk.Combobox(customize, textvariable=parameter, values=['PCE', 'Jsc', 'FF', 'Voc'], state='readonly')
        menu.config(font=('calibri', (10)), width=8)
        menu.place(x=100, y=78)

        Label(customize, text='Y-Label Rotation:', font=('calibri 13'), bg='white', fg='#28486B').place(x=250, y=30)
        self.xlabel_angle = IntVar()
        menu_3 = ttk.Combobox(customize, textvariable=self.xlabel_angle, values=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
        menu_3.config(font=('calibri', (10)), width=2)
        menu_3.place(x=450, y=34)

        Label(customize, text='Label Size:', font=('calibri 13 '), bg='white', fg='#28486B').place(x=250, y=70)
        self.label_size = IntVar()
        self.label_size.set(5)
        menu_4 = ttk.Combobox(customize, textvariable=self.label_size, values=[1, 2, 3, 4, 5, 6, 7, 8, 9])

        menu_4.config(font=('calibri', (10)), width=2)
        menu_4.place(x=450, y=74)

        CustomButton(customize, text='Box Plot', command=self.plot_it, width=8, borderwidth=0.5).place(x=15, y=120)
        CustomButton(customize, text='All in 1', command=self.plot_together, width=8, borderwidth=0.5).place(x=120,
                                                                                                            y=120)
        CustomButton(customize, text='Plot Hero JVs', command=self.hero_jvs, width=16, borderwidth=0.5).place(x=230,
                                                                                                           y=120)


        button_export_data = Button(self.box_plot, text='Export Data', command=self.export_data, borderwidth=0,
                                    bg='white', cursor='hand2')
        button_export_data.place(x=0, rely=0.88)
        button_start_over = Button(self.box_plot, text='Start Over', command=self.refresh, borderwidth=0, bg='white',
                                   cursor='hand2')
        button_start_over.place(x=0, rely=0.8)
        self.default_color_list = ['yellowgreen','rosybrown','turquoise','mediumpurple', 'lightblue', 'lightgreen','lightpink', 'grey']
        self.color_list = []
        self.entry_list = [] ##to store all the string variables of entry widget
        self.entry_widget_list = []  ## storing all the entry widget
        self.DF = pd.DataFrame()

    def show_frame(self, cont):  # to raise a selected frame
        frame = self.frames[cont]
        frame.tkraise()

    def auto_entry_generation(self, main_dir):
        for i in range(len(main_dir)):
            self.entry_list.append([''])  ##just a dummy place for it change in the next line
            self.entry_list[i] = StringVar()
            e = CustomEntry(self.box_plot, width=20, textvariable=self.entry_list[i])
            e.place(x=4, y=80 + 40*i, height=30)
            self.entry_widget_list.append(e)



    def get_directory(self):   # getting the directory
        dir = filedialog.askdirectory()
        if dir is not '':
            all_dirs_in_dir = [(dir + '/' + name) for name in os.listdir(dir) if
                           os.path.isdir(dir + '/' + name)]  ## did not use os.join in here as it joins with '\' not with '/'
            return all_dirs_in_dir







    def dataframe_creation(self):
        ## asking the user to choose path of the file to analyze
        ## making dataframe with all the data analyzed
        ## using the function dataframe() to make data frame and concatinate the output everytime you select one set of file
        main_dir = self.get_directory()
        ## what if user closes the filedialog without choosing file?
        ## self. filepath will be an empty string..

        if main_dir != None:
            self.auto_entry_generation(main_dir)


            for dir in main_dir:
                self.DF = pd.concat([self.DF, dataframe(dir)], axis=1)
                split_name = cut_string(dir,
                                        "/")  # for getting the name of the folder, check the function cut_string

                self.entry_list[self.split_count].set(split_name)

                self.split_count = self.split_count + 1

                ##to avoid any subdirectories which might have present in dir



    def plot_it(self):
        self.label_list = []

        for entry in self.entry_list:
           self.label_list.append(entry.get())

        x = self.split_count
        data = []
        data_rev = []
        data_fwd = []

        if parameter.get() == 'Jsc':

            if self.scan_choice_var.get() == 'Reverse':
                index_count = 2
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10

            elif self.scan_choice_var.get() == 'Forward':
                index_count = 3
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10

            elif self.scan_choice_var.get() == 'Together':
                index_count = 2
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 10

        elif parameter.get() == 'Voc':
            if self.scan_choice_var.get() == 'Reverse':
                index_count = 4
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Forward':
                index_count = 5
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Together':
                index_count = 4
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 10

        elif parameter.get() == 'FF':
            if self.scan_choice_var.get() == 'Reverse':
                index_count = 6
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Forward':
                index_count = 7
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Together':
                index_count = 6
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 10


        elif parameter.get() == 'PCE':
            if self.scan_choice_var.get() == 'Reverse':
                index_count = 8
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Forward':
                index_count = 9
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    data.append(lst)
                    index_count = index_count + 10
            elif self.scan_choice_var.get() == 'Together':
                index_count = 8
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 10

        ## plotting both scans in single graph
        f = Figure(figsize=(5, 3), dpi=150, tight_layout=True)

        if self.scan_choice_var.get() == 'Together':
            chart = f.add_subplot(111)
            chart.set_ylabel(self.optionlist[parameter.get()], fontsize=7)
            chart.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')

            ##plotting fwd scan
            chart.boxplot(data_fwd, meanline=True, widths=0.2, positions=[q for q in range(x)],
                          labels=['' for q in range(x)],
                          whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                          capprops=dict(color='red'), showfliers=False)

            ## plotting rev scans
            chart.boxplot(data_rev, meanline=True, widths=0.2, labels=['' for q in range(x)],
                          positions=[q + 0.3 for q in range(x)], showfliers=False)

            ##adding random jitters to the box plot
            for i in range(self.split_count):
                x_axis = np.random.normal(i, 0.03, size=len(data_fwd[i]))
                chart.plot(x_axis, data_fwd[i], 'r.', linestyle='none', ms=3)

                x_axis = np.random.normal(i + 0.3, 0.03, size=len(data_rev[i]))
                chart.plot(x_axis, data_rev[i], 'k.', linestyle='none', ms=3)
            # adding ticks in middle of rev and fwd boxes
            chart.set_xticks([x + 0.15 for x in range(self.split_count)])
            chart.set_xticklabels(self.label_list)

            hB, = chart.plot([1, 1], 'k-')
            hR, = chart.plot([1, 1], 'r-')
            chart.legend((hB, hR), ('Reverse Scans', 'Forward Scans'), prop={'size': 6})
            hR.set_visible(False)
            hB.set_visible(False)

        else:
            chart = f.add_subplot(111)
            chart.set_ylabel(self.optionlist[parameter.get()], fontsize=7)
            chart.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')

            chart.boxplot(data, meanline=True, labels=self.label_list, showfliers=False)
            for i in range(self.split_count):
                x_axis = np.random.normal(i + 1, 0.05, size=len(data[i]))
                chart.plot(x_axis, data[i], 'r.', linestyle='none', ms=4, )

        global canvas
        global toolbar
        try:
            canvas.get_tk_widget().place_forget()
            toolbar.place_forget()
        except:
            pass
        chart.tick_params(axis='x', length=0)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=300, y=50)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.configure(background = 'white')
        toolbar._message_label.config(background='white')
        toolbar.update()
        toolbar.place(x=350, y=0)




    def hero_jvs(self):
        self.label_list = []
        for entry in self.entry_list:
            self.label_list.append(entry.get())

        labels = self.label_list[0:self.split_count]
        f = Figure(figsize=(4, 3), dpi=140, tight_layout=True)

        chart = f.add_subplot(111, ylabel='Current Density (mA/cm$^2$)',
                              xlabel='Voltage (Volts)')

        chart.tick_params(axis='both', which='major', labelsize=5, direction='in')

        if self.scan_choice_var.get() == 'Reverse':

            ##plotting all the hero rev scans

            index_count_rev = 8

            for i in range(self.split_count):
                lst_rev = self.DF.iloc[:, index_count_rev]
                lst_rev = lst_rev.tolist()

                index = lst_rev.index(max(lst_rev))

                filename = self.DF.iloc[index, index_count_rev - 8]

                data = np.genfromtxt(filename, skip_header=10, dtype=float, delimiter='\t')  # loading txt file
                voltage_points = data[:, 0]
                current_points = data[:, 1]

                chart.plot(voltage_points, current_points, label=labels[i])
                if labels[i] != '':
                    chart.legend(prop={'size': self.label_size.get()})
                chart.set_ylim(bottom=0, auto=True)
                chart.set_xlim(left=0, auto = True)
                chart.yaxis.label.set_size(7)
                chart.xaxis.label.set_size(7)
                index_count_rev = index_count_rev + 10
        elif self.scan_choice_var.get() == 'Forward':
            ## plotting all the hero fwd scans
            index_count_fwd = 9

            for i in range(self.split_count):

                lst_fwd = self.DF.iloc[:, index_count_fwd]
                lst_fwd = lst_fwd.tolist()
                index = lst_fwd.index(max(lst_fwd))
                filename = self.DF.iloc[index, index_count_fwd - 8]

                data = np.genfromtxt(filename, skip_header=10, dtype=float, delimiter='\t')  # loading txt file
                voltage_points = data[:, 0]

                current_points = data[:, 1]

                chart.plot(voltage_points, current_points, label=labels[i])
                if labels[i] != '':
                    chart.legend(prop={'size': self.label_size.get()})
                chart.set_ylim(bottom=0, auto=True)
                chart.set_xlim(left=0, auto = True)
                chart.yaxis.label.set_size(7)
                chart.xaxis.label.set_size(7)
                index_count_fwd = index_count_fwd + 10
        else:
            messagebox.showinfo(message =
                'Together is not supported for this function.\nIf you wish to plot Rev and Fwd together, use Plot JV.')

        global canvas
        global toolbar
        try:
            canvas.get_tk_widget().place_forget()
            toolbar.place_forget()
        except:
            pass

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=470, y=50)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.config(background='white')
        toolbar._message_label.config(background='white')
        toolbar.update()
        toolbar.place(x=620, y=470)

    def plot_together(self):
        try:
            self.label_list = []

            for entry in self.entry_list:

                self.label_list.append(entry.get())

            x = self.split_count

            labels = self.label_list

            data = []
            data_rev = []
            data_fwd = []
            f = Figure(figsize=(7, 3.5), dpi=140, tight_layout=True)

            ax1 = f.add_subplot(222, ylabel='Current Density (mA/cm$^2$)', autoscale_on=True)
            ax2 = f.add_subplot(223, ylabel='Open Circuit Voltage (Volts)', autoscale_on=True)
            ax3 = f.add_subplot(224, ylabel='Fill Factor (%)', autoscale_on=True)
            ax4 = f.add_subplot(221, ylabel='Power Conversion Efficiency (%)', autoscale_on=True)

            ax_list = [ax1, ax2, ax3, ax4]
            for ax in ax_list:
                for tick in ax.get_xticklabels():
                    tick.set_rotation(self.xlabel_angle.get())
                ax.yaxis.label.set_size(6)
                ax.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')

            if self.scan_choice_var.get() == 'Reverse':
                index_count = 2
                for ax in ax_list:  # doing for all the subplots
                    data = []
                    for i in range(x):  # for all the splits within a sunplot
                        lst = self.DF.iloc[:, index_count]
                        lst = lst.dropna()
                        data.append(lst)
                        index_count = index_count + 10

                    # boxplot of a subplot
                    ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                               whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                               capprops=dict(color='red'), showfliers=False)
                    # adding jitters to the subplot
                    for i in range(x):
                        x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                        ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                    index_count = (index_count - (
                            x * 10)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.


            elif self.scan_choice_var.get() == 'Forward':
                index_count = 3
                for ax in ax_list:  # doing for all the subplots
                    data = []
                    for i in range(x):  # for all the splits within a subplot
                        lst = self.DF.iloc[:, index_count]
                        lst = lst.dropna()
                        data.append(lst)
                        index_count = index_count + 10
                    # boxplot of a subplot
                    ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                               whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                               capprops=dict(color='red'), showfliers=False)
                    # adding jitters to the subplot
                    for i in range(x):
                        x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                        ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                    index_count = (index_count - (
                            x * 10)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.


            elif self.scan_choice_var.get() == 'Together':
                index_count = 2
                for ax in ax_list:
                    data_rev = []
                    data_fwd = []
                    for i in range(x):
                        lst = self.DF.iloc[:, index_count]
                        lst = lst.dropna()
                        data_rev.append(lst)
                        lst = self.DF.iloc[:, index_count + 1]
                        lst = lst.dropna()
                        data_fwd.append(lst)
                        index_count = index_count + 10
                    ax.boxplot(data_fwd, meanline=True, widths=0.2, positions=[i for i in range(x)],
                               labels=['' for i in range(x)],
                               whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                               capprops=dict(color='red'), showfliers=False)

                    ax.boxplot(data_rev, meanline=True, widths=0.2, positions=[i + 0.3 for i in range(x)],
                               labels=['' for i in range(x)],
                               whiskerprops=dict(color='black'), boxprops=dict(color='black'),
                               capprops=dict(color='black'), showfliers=False)

                    for i in range(x):
                        x_axis = np.random.normal(i, 0.03, size=len(data_fwd[i]))
                        ax.plot(x_axis, data_fwd[i], 'r.', linestyle='none', ms=2)

                        x_axis = np.random.normal(i + 0.3, 0.03, size=len(data_rev[i]))
                        ax.plot(x_axis, data_rev[i], 'k.', linestyle='none', ms=2)
                    # placing ticks in between rev and forward box plaits
                    ax.set_xticks([i + 0.15 for i in range(x)])
                    ax.set_xticklabels(labels)

                    index_count = (index_count - (
                            x * 10)) + 2

                    # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.

            global canvas
            global toolbar
            try:
                canvas.get_tk_widget().place_forget()
                toolbar.place_forget()
            except:
                pass

            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().place(x=250, y=50)
            toolbar = NavigationToolbar2Tk(canvas, self)
            toolbar.config(background='white')
            toolbar._message_label.config(background='white')

            toolbar.update()
            toolbar.place(x=300, y=0)

        except:
            pass

    def export_data(self):
        try:

            location = filedialog.askdirectory()
            self.DF.to_csv(rf'{location}' + '/summary.csv', index=None, header=True)

        except:
            pass


    def refresh(self):

        self.DF = DataFrame()
        global canvas
        global toolbar
        try:
            canvas.get_tk_widget().place_forget()
            toolbar.place_forget()
        except:
            pass
        self.split_count = 0
        for e in self.entry_widget_list:
            e.place_forget()
        self.entry_list = []



class CustomButton(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        button = Button(self,relief ='solid', bg = 'white',*args, **kwargs)
        button.pack(fill="both", expand=2, padx=0.5, pady=0.5)
        self.configure(background = 'lightblue')

class CustomEntry(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        entry = Entry(self,relief ='sunken',*args, **kwargs)
        entry.pack(fill="both", expand=2, padx=1, pady=1)
        self.configure(background = '#28486B')

class ScrollableFrame(Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
