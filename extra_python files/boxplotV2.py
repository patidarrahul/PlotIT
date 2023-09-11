import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from Functions import *
from custom_widget import CustomEntry, CustomButton
class BoxPlotV2(tk.Tk):
    def __init__(self, address):
        super().__init__()
        self.addresses_to_plot = address
        self.total_splits = len(self.addresses_to_plot)
        self.DF = pd.DataFrame()
        self.dataframe_creation()

        ##figure frame
        screen_width = self.winfo_screenwidth()
        screen_width = int(0.75 * screen_width)
        screen_height = self.winfo_screenheight()
        screen_height = int(0.6 * screen_height)
        self.geometry(f'{screen_width}x{screen_height}+100+100')
        self.minsize(1300, 750)

        self.box_plot = tk.Frame(self, bg='white', relief='solid', borderwidth=0)
        self.box_plot.place(relx=0, rely=0, relwidth=1, relheight=0.75)
        self.wm_title('PlotIT 3.0')
        self.iconbitmap(r'icon.ico')

        ##customize_column
        customize = tk.Frame(self, bg='white', relief='solid', borderwidth=1)
        customize.place(relx=0, rely=0.75, relwidth=1, relheight=1)
        label_customize = tk.Label(self, text='Customize', bg='white', font='Calibri 14')
        label_customize.place(x=50, rely=0.72, relheight=0.06)



        tk.Label(customize, text='Scan:', font=('calibri 13'), bg='white', fg='#28486B').place(x=14, y=30)

        self.scan_choice = tk.StringVar()
        self.scan_choice = ttk.Combobox(customize, textvariable=self.scan_choice, values=['Reverse', 'Forward', 'Together'], state='readonly')
        self.scan_choice.place(x=100, y=34)
        self.scan_choice.config(font=('calibri', (10)), width=8)
        self.scan_choice.set('Reverse')





        self.optionlist = {'PCE': 'Power Conversion Efficiency (%)', 'Jsc': 'Current Density (mA/cm$^2$)',
                           'FF': 'Fill Factor (%)', 'Voc': 'Open Circuit Voltage (Volts)'}
        tk.Label(customize, text='Y-axis:', font=('calibri 12'), bg='white', fg='#28486B').place(x=14, y=74)

        self.parameter_var = tk.StringVar()


        self.parameter = ttk.Combobox(customize, textvariable=self.parameter_var, values=['PCE', 'Jsc', 'FF', 'Voc'], state='readonly')
        self.parameter.config(font=('calibri', (10)), width=8)
        self.parameter.place(x=100, y=78)
        self.parameter.set('PCE')

        tk.Label(customize, text='X-Label Rotation:', font=('calibri 13'), bg='white', fg='#28486B').place(x=250, y=30)
        self.xlabel_angle_var = tk.IntVar()
        self.xlabel_angle = ttk.Combobox(customize, textvariable=self.xlabel_angle_var, values=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
        self.xlabel_angle.config(font=('calibri', (10)), width=2)
        self.xlabel_angle.place(x=450, y=34)
        self.xlabel_angle.set(0)

        tk.Label(customize, text='Label Size:', font=('calibri 13 '), bg='white', fg='#28486B').place(x=250, y=70)
        self.label_size_var = tk.IntVar()

        self.label_size= ttk.Combobox(customize, textvariable=self.label_size_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 13])

        self.label_size.config(font=('calibri', (10)), width=2)
        self.label_size.place(x=450, y=74)
        self.label_size.set(5)
        CustomButton(customize, text='Box Plot', command=self.plot_it, width=8, borderwidth=0.5).place(x=15, y=120)
        CustomButton(customize, text='All in 1', command=self.plot_together, width=8, borderwidth=0.5).place(x=120,
                                                                                                            y=120)




        button_export_data = tk.Button(customize, text='Export Data', font = 'calibri 14',command=self.export_data, borderwidth=0,
                                    bg='white', cursor='hand2')
        button_export_data.place(relx=0.88, rely=0.02)

        resistance_frame =tk.Frame(customize, bg='white', relief='solid', borderwidth=0.5)
        resistance_frame.place(x = 520, y = 0, relheight = 1, relwidth = 0.5)

        tk.Label(resistance_frame, text='Y-axis (Series Resistance) ', font=('calibri 12'), bg='white', fg='#28486B').place(x=20, y=30)
        self.series_resistance_var = tk.IntVar()
        self.series_resistance_limit = ttk.Combobox(resistance_frame, textvariable=self.series_resistance_var)
        self.series_resistance_limit.place(x=20, y=60)
        self.series_resistance_limit.set(200)

        tk.Label(resistance_frame, text='Y-axis (Shunt Resistance) ', font=('calibri 12'), bg='white', fg='#28486B').place(x=20, y=110)
        self.shunt_resistance_var = tk.IntVar()

        self.shunt_resistance_limit = ttk.Combobox(resistance_frame, textvariable=self.shunt_resistance_var)
        self.shunt_resistance_limit.place(x=20, y=140)
        self.shunt_resistance_limit.set(200000)


        CustomButton(resistance_frame, text='Resistance Plot', command=self.resistance_plot, width=8, borderwidth=0.5).place(
            x=300,
            y=50, width = 150)




        self.entry_list = [cut_string(i, '/') for i in self.addresses_to_plot ]##to store all the string variables of entry widget
        self.entry_list_var = []
        self.entry_widget_list = []

        self.auto_entry_generation()
        self.plot_it()

    def dataframe_creation(self):
        ## asking the user to choose path of the file to analyze
        ## making dataframe with all the data analyzed
        ## using the function dataframe() to make data frame and concatinate the output everytime you select one set of file
        self.main_dir = self.addresses_to_plot


        ## what if user closes the filedialog without choosing file?
        ## self. filepath will be an empty string..

        if self.main_dir != None:


            for dir in self.main_dir:
                self.DF = pd.concat([self.DF, dataframe(dir)], axis=1)
                split_name = cut_string(dir,
                                        "/")  # for getting the name of the folder, check the function cut_string


                ##to avoid any subdirectories which might have present in dir

    def auto_entry_generation(self):
        tk.Label(self.box_plot, text = 'Labels:',font=('calibri 12'), bg='white', fg='#28486B' ).place(x=4, y = 50)
        for i in range(len(self.entry_list)):
            self.entry_list_var.append([''])  ##just a dummy place for it change in the next line
            self.entry_list_var[i] = tk.StringVar(self)
            e = CustomEntry(self.box_plot, width=20, textvariable=self.entry_list_var[i])
            e.place(x=4, y=80 + 40 * i, height=30)
            self.entry_widget_list.append(e)
        for i in range(len(self.entry_list)):
            self.entry_list_var[i].set(self.entry_list[i])



    def plot_it(self):
        self.label_list = []

        for i in range(len(self.entry_list_var)):
           self.label_list.append(self.entry_list_var[i].get())

        x = self.total_splits
        data = []
        data_rev = []
        data_fwd = []


        if self.parameter.get() == 'Jsc':

            if self.scan_choice.get() == 'Reverse':
                index_count = 1
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13

            elif self.scan_choice.get() == 'Forward':

                index_count = 2
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13

            elif self.scan_choice.get() == 'Together':
                index_count = 1
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13

        elif self.parameter.get() == 'Voc':
            if self.scan_choice.get() == 'Reverse':
                index_count = 3
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Forward':
                index_count = 4
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Together':
                index_count = 3
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13

        elif self.parameter.get() == 'FF':
            if self.scan_choice.get() == 'Reverse':
                index_count = 5
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Forward':
                index_count = 6
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Together':
                index_count = 5
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13


        elif self.parameter.get() == 'PCE':
            if self.scan_choice.get() == 'Reverse':
                index_count = 7
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()

                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Forward':
                index_count = 8
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Together':
                index_count = 7
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13

        ## plotting both scans in single graph
        f = Figure(figsize=(5, 3), dpi=150, tight_layout=True)

        if self.scan_choice.get() == 'Together':
            chart = f.add_subplot(111)
            chart.set_ylabel(self.optionlist[self.parameter.get()], fontsize=7)
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
            for i in range(self.total_splits):
                x_axis = np.random.normal(i, 0.03, size=len(data_fwd[i]))
                chart.plot(x_axis, data_fwd[i], 'r.', linestyle='none', ms=3)

                x_axis = np.random.normal(i + 0.3, 0.03, size=len(data_rev[i]))
                chart.plot(x_axis, data_rev[i], 'k.', linestyle='none', ms=3)
            # adding ticks in middle of rev and fwd boxes
            chart.set_xticks([x + 0.15 for x in range(self.total_splits)])
            chart.set_xticklabels(self.label_list)

            hB, = chart.plot([1, 1], 'k-')
            hR, = chart.plot([1, 1], 'r-')
            chart.legend((hB, hR), ('Reverse Scans', 'Forward Scans'), prop={'size': 6})
            hR.set_visible(False)
            hB.set_visible(False)

        else:
            chart = f.add_subplot(111)
            chart.set_ylabel(self.optionlist[self.parameter.get()], fontsize=7)
            chart.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')

            chart.boxplot(data, meanline=True, labels=self.label_list, showfliers=False)
            for i in range(self.total_splits):
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






    def plot_together(self):
        try:
            self.label_list = []

            for i in range(len(self.entry_list_var)):
                self.label_list.append(self.entry_list_var[i].get())

            x = self.total_splits

            labels = self.label_list

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

            if self.scan_choice.get() == 'Reverse':
                index_count = 1
                for ax in ax_list:  # doing for all the subplots
                    data = []
                    for i in range(x):  # for all the splits within a sunplot
                        lst = self.DF.iloc[:, index_count]
                        lst = lst.dropna()
                        data.append(lst)
                        index_count = index_count + 13

                    # boxplot of a subplot
                    ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                               whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                               capprops=dict(color='red'), showfliers=False)
                    # adding jitters to the subplot
                    for i in range(x):
                        x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                        ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                    index_count = (index_count - (
                            x * 13)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.


            elif self.scan_choice.get() == 'Forward':
                index_count = 2
                for ax in ax_list:  # doing for all the subplots
                    data = []
                    for i in range(x):  # for all the splits within a subplot
                        lst = self.DF.iloc[:, index_count]
                        lst = lst.dropna()
                        data.append(lst)
                        index_count = index_count + 13
                    # boxplot of a subplot
                    ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                               whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                               capprops=dict(color='red'), showfliers=False)
                    # adding jitters to the subplot
                    for i in range(x):
                        x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                        ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                    index_count = (index_count - (
                            x * 13)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.


            elif self.scan_choice.get() == 'Together':
                index_count = 1
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
                        index_count = index_count + 13
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
                            x * 13)) + 2

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

    def resistance_plot(self):
        self.label_list = []

        for i in range(len(self.entry_list_var)):
            self.label_list.append(self.entry_list_var[i].get())

        x = self.total_splits

        labels = self.label_list

        f = Figure(figsize=(8, 3.5), dpi=140, tight_layout=True)

        ax1 = f.add_subplot(121, ylabel='Series Resitance', autoscale_on=True)
        ax2 = f.add_subplot(122, ylabel='Shunt Resistance', autoscale_on=True)


        ax_list = [ax1, ax2]
        for ax in ax_list:
            for tick in ax.get_xticklabels():
                tick.set_rotation(self.xlabel_angle.get())
            ax.yaxis.label.set_size(6)
            ax.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')

        if self.scan_choice.get() == 'Reverse':
            index_count = 9
            for ax in ax_list:  # doing for all the subplots
                data = []
                for i in range(x):  # for all the splits within a sunplot
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data.append(lst)
                    index_count = index_count + 13

                # boxplot of a subplot

                ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                            whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                            capprops=dict(color='red'), showfliers=False)
                # adding jitters to the subplot
                for i in range(x):
                    x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                    ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                index_count = (index_count - (
                        x * 13)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.
            ax_list[0].set_ylim(0,float(self.series_resistance_limit.get()))
            ax_list[1].set_ylim(0, float(self.shunt_resistance_limit.get()))


        elif self.scan_choice.get() == 'Forward':
            index_count = 10
            for ax in ax_list:  # doing for all the subplots
                data = []
                for i in range(x):  # for all the splits within a subplot
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data.append(lst)
                    index_count = index_count + 13
                # boxplot of a subplot
                ax.boxplot(data, meanline=True, widths=0.2, positions=[i for i in range(x)], labels=labels,
                           whiskerprops=dict(color='red'), boxprops=dict(color='red'),
                           capprops=dict(color='red'), showfliers=False)
                # adding jitters to the subplot
                for i in range(x):
                    x_axis = np.random.normal(i, 0.03, size=len(data[i]))
                    ax.plot(x_axis, data[i], 'r.', linestyle='none', ms=2)

                index_count = (index_count - (
                        x * 13)) + 2  # a liitle equation to adjust the index count back to the next graph where x is number of time the increment takes place.
            ax_list[0].set_ylim(0, float(self.series_resistance_limit.get()))
            ax_list[1].set_ylim(0, float(self.shunt_resistance_limit.get()))

        elif self.scan_choice.get() == 'Together':
            index_count = 9
            for ax in ax_list:
                data_rev = []
                data_fwd = []
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data_rev.append(lst)
                    lst = self.DF.iloc[:, index_count + 1]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data_fwd.append(lst)
                    index_count = index_count + 13
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
                        x * 13)) + 2
            ax_list[0].set_ylim(0, float(self.series_resistance_limit.get()))
            ax_list[1].set_ylim(0, float(self.shunt_resistance_limit.get()))
        global canvas
        global toolbar
        try:
            canvas.get_tk_widget().place_forget()
            toolbar.place_forget()
        except:
            pass

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=200, y=50)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.config(background='white')
        toolbar._message_label.config(background='white')

        toolbar.update()
        toolbar.place(x=300, y=0)

if __name__ == '__main__':
    root = BoxPlotV2(address)  # Replace 'address' with the desired input address
    root.mainloop()






