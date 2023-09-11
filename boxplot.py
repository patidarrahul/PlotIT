import glob
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import statistics
import pandas as pd
from custom_widget import CustomEntry, CustomButton
import numpy as np
from matplotlib.patches import Patch
import seaborn as sns
from Functions import dataframe, cut_string


class JV(tk.Frame):
    def __init__(self, master, address):
        super().__init__(master)
        self.address_to_plot = address
        self.main_dir = address
        self.configure(bg='white')

        self.jv_frame = tk.Frame(self, bg='white')
        self.jv_frame.grid(row=0, column=0, sticky='nw')

        self.jv_frame_label = tk.Frame(self, bg='white')
        self.jv_frame_label.grid(row=0, column=1, sticky='n')

        tk.Label(self.jv_frame_label, text='Labels:', font=('calibri 15'), bg='white', fg='#28486B').grid(row=0, column=0,
                                                                                                          padx=5,
                                                                                                          pady=5,
                                                                                                          sticky='w')

        button_frame = tk.Frame(self, bg='white')
        button_frame.grid(row=1, column=0, sticky='nw')

        tk.Label(button_frame, text='Scan:', font=('calibri 15'), bg='white', fg='#28486B').grid(row=0,
                                                                                                 column=0,
                                                                                                 padx=10,
                                                                                                 pady=10,
                                                                                                 sticky='w')

        self.scan_choice_var = tk.StringVar()
        self.scan_choice = ttk.Combobox(button_frame, textvariable=self.scan_choice_var,
                                        values=['Reverse', 'Forward', 'Together'], state='readonly')
        self.scan_choice.grid(row=0, column=1, pady=10, sticky='w')
        self.scan_choice.config(font=('calibri', (12)), width=8)
        self.scan_choice.set('Together')

        CustomButton(button_frame, text='Apply', font=('calibri 12'), command=self.hero_jv_plot,
                     width=10, borderwidth=0.5).grid(row=1, column=0, padx=10, pady=10)
        self.entry_list_jv_var = []
        self.entry_widget_list_jv = []
        self.entry_list = [cut_string(i, '\\') for i in self.address_to_plot]
        self.auto_entry_generation()
        self.hero_jv_plot()

    def auto_entry_generation(self):

        for i in range(len(self.main_dir)):
            # just a dummy place for it change in the next line
            self.entry_list_jv_var.append([''])
            self.entry_list_jv_var[i] = tk.StringVar()
            e = CustomEntry(self.jv_frame_label, width=20, font=(
                'calibri 12'), textvariable=self.entry_list_jv_var[i])
            e.grid(row=i+1, column=0, padx=5, pady=5, sticky='w')
            self.entry_widget_list_jv.append(e)
        for i in range(len(self.main_dir)):
            self.entry_list_jv_var[i].set(self.entry_list[i])

    def hero_jv_plot(self):
        files_to_plot = []
        for dir in self.main_dir:
            files = glob.glob(f'{dir}/*.SEQ')
            pce_rev = {}  # defining arrays with key = file name and value = respective scan pce
            pce_fwd = {}
            for file in files:
                with open(file) as f:
                    split_file = []
                    for line in f:
                        line = line.split('\t')
                        split_file.append(line)

                    if split_file[28][3] == 'Light':  # filtering the light current
                        # adress of rev_pce
                        pce_rev[file] = float(split_file[28][9])
                        # adress of fwd_pce
                        pce_fwd[file] = float(split_file[29][9])

            if statistics.mean(list(pce_rev.values())) >= statistics.mean(list(pce_fwd.values())):
                # Get the key corresponding to the maximum value
                max_key_rev = max(pce_rev, key=pce_rev.get)
                files_to_plot.append(str(max_key_rev))
            else:
                # Get the key corresponding to the maximum value
                max_key_fwd = max(pce_fwd, key=pce_fwd.get)
                files_to_plot.append(str(max_key_fwd))

        fig, ax = plt.subplots(figsize=(9, 5))

        if self.scan_choice_var.get() == 'Together':
            for i, file in enumerate(files_to_plot):
                data = np.genfromtxt(file, skip_header=35,
                                     dtype=float, delimiter='\t')
                xaxis_rev = data[:, 0]  # First column
                yaxis_rev = data[:, 1]  # Second column
                xaxis_fwd = data[:, 4]
                yaxis_fwd = data[:, 5]
                ax.plot(xaxis_rev, yaxis_rev,
                        label=f'Reverse {self.entry_list_jv_var[i].get()}')
                ax.scatter(xaxis_fwd, yaxis_fwd, linestyle='-',
                           label=f'Forward {self.entry_list_jv_var[i].get()}')

        elif self.scan_choice_var.get() == 'Reverse':
            for i, file in enumerate(files_to_plot):
                data = np.genfromtxt(file, skip_header=35,
                                     dtype=float, delimiter='\t')
                xaxis_rev = data[:, 0]  # First column
                yaxis_rev = data[:, 1]  # Second column
                ax.plot(xaxis_rev, yaxis_rev,
                        label=self.entry_list_jv_var[i].get())

        elif self.scan_choice_var.get() == 'Forward':
            for i, file in enumerate(files_to_plot):
                data = np.genfromtxt(file, skip_header=35,
                                     dtype=float, delimiter='\t')

                xaxis_fwd = data[:, 4]
                yaxis_fwd = data[:, 5]
                ax.plot(xaxis_fwd, yaxis_fwd,
                        label=self.entry_list_jv_var[i].get())

        ax.set_ylim(0)
        ax.set_xlim(0)
        ax.set_xlabel('Voltage (Volts)')
        ax.set_ylabel('Current Density (mA/cm$^2$)')
        ax.tick_params(axis='both', direction='in')

        fig.subplots_adjust(right=0.7)

        legend = fig.legend(loc='upper left', bbox_to_anchor=(
            0.7, 0.895), bbox_transform=plt.gcf().transFigure)
        frame = legend.get_frame()
        frame.set_edgecolor('black')
        # Display the plot

        global jv_canvas
        try:
            jv_canvas.get_tk_widget().grid_remove()

        except:
            pass

        jv_canvas = FigureCanvasTkAgg(fig, self.jv_frame)
        jv_canvas.get_tk_widget().grid(row=0, column=0)

        # Display the plot
        jv_canvas.draw()


class BoxPlot(tk.Frame):
    def __init__(self, master, address):
        super().__init__(master)

        self.addresses_to_plot = address
        self.main_dir = address
        self.total_splits = len(self.addresses_to_plot)
        self.DF = pd.DataFrame()
        self.dataframe_creation()
        self.configure(bg='white')

        self.scrollabel_canvas = tk.Canvas(self, background='white')
        scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self.scrollabel_canvas.yview)
        scrollable_frame = tk.Frame(self.scrollabel_canvas, bg='white')
        self.scrollabel_canvas.bind(
            '<MouseWheel>', lambda event: self.scrollabel_canvas.yview_scroll(event.delta/60, 'units'))

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.scrollabel_canvas.configure(
                scrollregion=self.scrollabel_canvas.bbox("all")
            )
        )

        self.scrollabel_canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw")
        self.scrollabel_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.scrollabel_canvas.pack(side="left", fill="both", expand=True)

        self.scrollabel_canvas.bind("<MouseWheel>", self.on_mousewheel)

        # boxplot_frame

        self.box_plot_frame = tk.Frame(scrollable_frame, bg='white')
        self.box_plot_frame.grid(row=0, column=0, sticky='nw')

        # customize_column for box plot
        customize_frame = tk.Frame(scrollable_frame, bg='white')
        customize_frame.grid(row=1, column=0, sticky='sw', pady=20)

        tk.Label(customize_frame, text='Scan:', font=('calibri 15'), bg='white', fg='#28486B').grid(row=0, column=0, padx=10, pady=5,
                                                                                                    sticky='w')

        self.scan_choice = tk.StringVar()
        self.scan_choice = ttk.Combobox(customize_frame, textvariable=self.scan_choice,
                                        values=['Reverse', 'Forward', 'Together'], state='readonly')
        self.scan_choice.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.scan_choice.config(font=('calibri', (12)), width=8)
        self.scan_choice.set('Reverse')

        self.optionlist = {'PCE': 'Power Conversion Efficiency (%)', 'Jsc': 'Current Density (mA/cm$^2$)',
                           'FF': 'Fill Factor (%)', 'Voc': 'Open Circuit Voltage (Volts)',
                           'Series': 'Series Resitance (\u03A9)', 'Shunt': 'Shunt Resitance (\u03A9)'}
        tk.Label(customize_frame, text='Y-axis:', font=('calibri 15'), bg='white', fg='#28486B').grid(row=1, column=0, padx=10, pady=5,
                                                                                                      sticky='w')

        self.parameter_var = tk.StringVar()

        self.parameter = ttk.Combobox(customize_frame, textvariable=self.parameter_var,
                                      values=['PCE', 'Jsc', 'FF',
                                              'Voc', 'Series', 'Shunt'],
                                      state='readonly')
        self.parameter.config(font=('calibri', (12)), width=8)
        self.parameter.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.parameter.set('PCE')

        tk.Label(customize_frame, text='X-Label Rotation:', font=('calibri 15'),
                 bg='white', fg='#28486B').grid(row=0, column=2, padx=10, pady=5, sticky='w')
        self.xlabel_angle_var = tk.IntVar()
        self.xlabel_angle = ttk.Combobox(customize_frame, textvariable=self.xlabel_angle_var,
                                         values=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
        self.xlabel_angle.config(font=('calibri', (12)), width=2)
        self.xlabel_angle.grid(row=0, column=3, padx=10, pady=5, sticky='w')
        self.xlabel_angle.set(0)

        tk.Label(customize_frame, text='Label Size:', font=('calibri 15 '),
                 bg='white', fg='#28486B').grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.label_size_var = tk.IntVar()

        self.label_size = ttk.Combobox(
            customize_frame, textvariable=self.label_size_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 13])

        self.label_size.config(font=('calibri', (12)), width=2)
        self.label_size.grid(row=1, column=3, padx=10, pady=5, sticky='w')
        self.label_size.set(5)

        CustomButton(customize_frame, text='Y-Values', font=('calibri', (12)),
                     command=self.y_values_range, width=10, borderwidth=0.5).grid(row=3, column=0, padx=5, pady=5, sticky='w')

        CustomButton(customize_frame, text='Box Plot', font=('calibri', (12)), command=self.plot_it,
                     width=10, borderwidth=0.5).grid(row=4, column=0, padx=5, pady=5, sticky='w')
        CustomButton(customize_frame, text='Together', font=('calibri', (12)), command=self.plot_together,
                     width=10, borderwidth=0.5).grid(row=4, column=1, padx=5, pady=5, sticky='w')
        CustomButton(customize_frame, text="Save Graph", font=('calibri', (12)), command=self.save_graph,
                     width=10, borderwidth=0.5).grid(row=5, column=0, padx=5, pady=5, sticky='w')

        button_export_data = tk.Button(customize_frame, text='Export Data', font='calibri 15', command=self.export_data,
                                       borderwidth=0,
                                       bg='white', cursor='hand2')
        button_export_data.grid(row=6, column=0, padx=5, pady=20, sticky='sw')

        # adding entry widget to get the labels for the figure from
        self.entry_list = [cut_string(i, '\\') for i in
                           self.addresses_to_plot]  # to store all the string variables of entry widget
        self.entry_list_var = []
        self.entry_widget_list = []

        # label frame
        self.label_frame_box_plot = tk.Frame(scrollable_frame, bg='white')
        self.label_frame_box_plot.grid(row=0, column=1, sticky='n')
        tk.Label(self.label_frame_box_plot, text='Labels:', font=('calibri 15'), bg='white', fg='#28486B').grid(row=0, column=0,
                                                                                                                padx=5,
                                                                                                                pady=10,
                                                                                                                sticky='w')

        # Generate a list of colors using cm.rainbow colormap

        self.color_choice_fill = sns.color_palette('pastel')

        self.color_choice_border = sns.color_palette('deep')

        self.auto_entry_generation_box()

        # generating common fig and axes variable
        self.fig, self.axes = plt.subplots()

        # set the status of the funtion
        self.plot_it_executed = False
        self.plot_together_executed = False
        self.apply_changes_to_y_values_executed = False

        self.plot_it()

    def on_mousewheel(self, event):
        self.scrollabel_canvas.yview_scroll(
            int(-1 * (event.delta / 60)), "units")

    def dataframe_creation(self):
        # asking the user to choose path of the file to analyze
        # making dataframe with all the data analyzed
        # using the function dataframe() to make data frame and concatinate the output everytime you select one set of file
        self.main_dir = self.addresses_to_plot

        # what if user closes the filedialog without choosing file?
        # self. filepath will be an empty string..

        if self.main_dir != None:

            for dir in self.main_dir:
                self.DF = pd.concat([self.DF, dataframe(dir)], axis=1)

                split_name = cut_string(dir,
                                        "/")  # for getting the name of the folder, check the function cut_string

                # to avoid any subdirectories which might have present in dir

    def auto_entry_generation_box(self):
        for i in range(len(self.entry_list)):
            # just a dummy place for it change in the next line
            self.entry_list_var.append([''])
            self.entry_list_var[i] = tk.StringVar()
            e_box = CustomEntry(self.label_frame_box_plot, font=(
                'calibri', 12), width=20, textvariable=self.entry_list_var[i])
            e_box.grid(row=i + 1, column=0, padx=5, pady=5, sticky='w')
            # e.configure(font=('calibri', (10)), width=2)
            self.entry_widget_list.append(e_box)
        for i in range(len(self.main_dir)):
            self.entry_list_var[i].set(self.entry_list[i])

    def plot_it(self, *args, **kwargs):
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
        elif self.parameter.get() == 'Series':
            if self.scan_choice.get() == 'Reverse':
                index_count = 9
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Forward':
                index_count = 10
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Together':
                index_count = 9
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13
        elif self.parameter.get() == 'Shunt':
            if self.scan_choice.get() == 'Reverse':
                index_count = 11
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    lst = [int(float(i)) for i in lst]
                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Forward':
                index_count = 12
                for i in range(x):
                    lst = self.DF.iloc[:, index_count]
                    lst = lst.dropna()
                    data.append(lst)
                    index_count = index_count + 13
            elif self.scan_choice.get() == 'Together':
                index_count = 11
                for i in range(x):
                    lst_rv = self.DF.iloc[:, index_count]
                    lst_rv = lst_rv.dropna()
                    lst_fwd = self.DF.iloc[:, index_count + 1]
                    lst_fwd = lst_fwd.dropna()
                    data_rev.append(lst_rv)
                    data_fwd.append(lst_fwd)

                    index_count = index_count + 13

        # plotting both scans in single graph

        self.fig, self.axes = plt.subplots(figsize=(4.5, 2.8), dpi=150)

        if self.scan_choice.get() == 'Together':

            self.axes.set_ylabel(
                self.optionlist[self.parameter.get()], fontsize=7)
            self.axes.tick_params(axis='both', which='major',
                                  labelsize=self.label_size.get(), direction='in')

            try:
                if self.apply_changes_to_y_values_executed:

                    if self.parameter.get() == 'PCE':
                        self.axes.set_ylim(kwargs.get(
                            'pce_ymin'), kwargs.get('pce_ymax'))

                    elif self.parameter.get() == 'Jsc':
                        self.axes.set_ylim(kwargs.get(
                            'jsc_ymin'), kwargs.get('jsc_ymax'))

                    elif self.parameter.get() == 'Voc':
                        self.axes.set_ylim(kwargs.get(
                            'voc_ymin'), kwargs.get('voc_ymax'))

                    elif self.parameter.get() == 'FF':
                        self.axes.set_ylim(kwargs.get(
                            'ff_ymin'), kwargs.get('ff_ymax'))

                    elif self.parameter.get() == 'Series':
                        self.axes.set_ylim(kwargs.get(
                            'shunt_ymin'), kwargs.get('series_ymax'))

                    elif self.parameter.get() == 'Shunt':
                        self.axes.set_ylim(kwargs.get(
                            'shunt_ymin'), kwargs.get('shunt_ymax'))
            except:
                messagebox.showinfo(title='Error',
                                    message='Please make sure the values are integer')

            # plotting data_rev
            for i, scan_data_rev in enumerate(data_rev):
                self.axes.boxplot(scan_data_rev, showmeans=False, positions=[i],
                                  widths=0.2, showfliers=False,
                                  boxprops=dict(
                                      color=self.color_choice_border[i]),
                                  medianprops=dict(
                                      color=self.color_choice_border[i]),
                                  whiskerprops=dict(
                                      color=self.color_choice_border[i]),
                                  capprops=dict(color=self.color_choice_border[i]))
            # adding jitters
            for i in range(self.total_splits):
                x_axis = np.random.normal(i, 0.05, size=len(data_fwd[i]))
                self.axes.plot(x_axis, data_rev[i], color=self.color_choice_border[i], marker='o', linestyle='none', ms=2,
                               label=self.label_list)

            # plotting data_fwd
            for i, scan_data_fwd in enumerate(data_fwd):
                self.axes.boxplot(scan_data_fwd, showmeans=False, positions=[i + 0.3],
                                  patch_artist=True, widths=0.2, showfliers=False,
                                  boxprops=dict(
                                      facecolor=self.color_choice_fill[i], color=self.color_choice_border[i]),
                                  medianprops=dict(
                                      color=self.color_choice_border[i]),
                                  whiskerprops=dict(
                                      color=self.color_choice_border[i]),
                                  capprops=dict(color=self.color_choice_border[i]))
            # adding jitters
            for i in range(self.total_splits):
                x_axis = np.random.normal(i + 0.3, 0.05, size=len(data_fwd[i]))
                self.axes.plot(x_axis, data_fwd[i], color=self.color_choice_border[i], marker='o', linestyle='none', ms=2,
                               label=self.label_list)

            group_labels = []
            for i in range(len(self.entry_list_var)):
                group_labels.append(self.entry_list_var[i].get())

            self.axes.set_xticks([i + 0.15 for i in range(self.total_splits)])
            self.axes.set_xticklabels(group_labels)

            legend_handles = [Patch(facecolor='none', edgecolor='lightgrey', label='Reverse Scan'),
                              Patch(facecolor='lightgrey', edgecolor='lightgrey', label='Forward Scan')]
            # Adjust the top margin to make space for the legend
            self.fig.subplots_adjust(top=0.92)
            # f.legend(legend_handles,  loc='upper center', ncol=len(legend_labels),
            #           bbox_to_anchor=(0.5, 1), bbox_transform=f.transFigure, fancybox=True, shadow=True)
            self.fig.legend(handles=legend_handles, loc='upper center',
                            ncol=2, fontsize='6', frameon=False)

        else:

            self.axes.set_ylabel(
                self.optionlist[self.parameter.get()], fontsize=7)
            self.axes.tick_params(axis='both', which='major',
                                  labelsize=self.label_size.get(), direction='in')

            try:
                if self.apply_changes_to_y_values_executed:

                    if self.parameter.get() == 'PCE':
                        self.axes.set_ylim(kwargs.get(
                            'pce_ymin'), kwargs.get('pce_ymax'))

                    elif self.parameter.get() == 'Jsc':
                        self.axes.set_ylim(kwargs.get(
                            'jsc_ymin'), kwargs.get('jsc_ymax'))

                    elif self.parameter.get() == 'Voc':
                        self.axes.set_ylim(kwargs.get(
                            'voc_ymin'), kwargs.get('voc_ymax'))

                    elif self.parameter.get() == 'FF':
                        self.axes.set_ylim(kwargs.get(
                            'ff_ymin'), kwargs.get('ff_ymax'))

                    elif self.parameter.get() == 'Series':
                        self.axes.set_ylim(kwargs.get(
                            'shunt_ymin'), kwargs.get('series_ymax'))

                    elif self.parameter.get() == 'Shunt':
                        self.axes.set_ylim(kwargs.get(
                            'shunt_ymin'), kwargs.get('shunt_ymax'))

            except:
                messagebox.showinfo(
                    title='Error', message='Please make sure the values are integer')

            # for tick in self.axes.get_xticklabels():
            #     print('..........................................')
            #     print(tick, type(tick))
            #     print(self.xlabel_angle.get())
            #     tick.set_rotation(self.xlabel_angle.get())

            for i, scan in enumerate(data):
                box1 = self.axes.boxplot(scan, showmeans=False, positions=[i],
                                         patch_artist=True, widths=0.2, showfliers=False,
                                         boxprops=dict(
                                             facecolor=self.color_choice_fill[i], color=self.color_choice_border[i]),
                                         medianprops=dict(
                                             color=self.color_choice_border[i]),
                                         whiskerprops=dict(
                                             color=self.color_choice_border[i]),
                                         capprops=dict(color=self.color_choice_border[i]))

            for i in range(self.total_splits):
                x_axis = np.random.normal(i, 0.05, size=len(data[i]))
                self.axes.plot(x_axis, data[i], color=self.color_choice_border[i], marker='o', linestyle='none', ms=2,
                               label=self.label_list)

            group_labels = []
            for i in range(len(self.entry_list_var)):
                group_labels.append(self.entry_list_var[i].get())

            self.axes.set_xticks([i + 0.15 for i in range(self.total_splits)])
            self.axes.set_xticklabels(group_labels)
        global canvas
        try:
            canvas.get_tk_widget().grid_remove()

        except:
            pass
        self.axes.tick_params(axis='x', length=0)
        canvas = FigureCanvasTkAgg(self.fig, self.box_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        self.plot_it_executed = True
        self.plot_together_executed = False

    def plot_together(self, color1='lightblue', color2='lightgreen', *args, **kwargs):
        # Generate sample data
        print('Hello')
        dataf = self.DF
        # 13 is the number of columns per data set
        num_groups = int(len(dataf.columns) / 13)
        data_pce = []
        data_jsc = []
        data_voc = []
        data_ff = []

        param = ['Power Conversion Efficiency (%)', 'Current Density (mA/cm$^2$)', 'Open Circuit Voltage (Voc)',
                 'Fill Factor (%)']
        # getting rerverse anf forward data from the csv file for each group and for each parameter and appending it into the main list (data_jsc)
        for num_groups_index in range(num_groups):
            index = num_groups_index * 13
            jsc = [(dataf.iloc[:, index + 1]).dropna().tolist(),
                   (dataf.iloc[:, index + 2]).dropna().tolist()]
            data_jsc.append(jsc)
            voc = [(dataf.iloc[:, index + 3]).dropna().tolist(),
                   (dataf.iloc[:, index + 4]).dropna().tolist()]
            data_voc.append(voc)
            ff = [(dataf.iloc[:, index + 5]).dropna().tolist(),
                  (dataf.iloc[:, index + 6]).dropna().tolist()]
            data_ff.append(ff)
            pce = [(dataf.iloc[:, index + 7]).dropna().tolist(),
                   (dataf.iloc[:, index + 8]).dropna().tolist()]
            data_pce.append(pce)
        data = [data_pce, data_jsc, data_voc, data_ff]

        group_labels = []
        for i in range(len(self.entry_list_var)):
            group_labels.append(self.entry_list_var[i].get())

        subgroup_labels = ['Reverese', 'Forward']
        global axes
        # Create the figure and axes
        self.fig, self.axes = plt.subplots(
            nrows=2, ncols=2, figsize=(12, 8), dpi=80)

        # Flatten the axes array for easier indexing
        self.axes = self.axes.flatten()

        colors = [color1, color2]

        # Iterate over the param
        for param_index in range(len(param)):
            ax = self.axes[param_index]  # Get the corresponding axis

            # Generate sample data for the set
            param_data = data[param_index]

            # Calculate the positions of the groups and subgroups
            group_positions = np.arange(num_groups)

            for i, scan_data in enumerate(param_data):
                # Calculate the positions of the subgroups within the group
                # subgroup_positions = group_positions[i]
                position1 = i
                position2 = i + 0.3

                # Iterate over the subgroups
                ax.boxplot(scan_data[0], showmeans=False,
                           positions=[position1], patch_artist=True, widths=0.2, showfliers=False, boxprops=dict(facecolor=colors[0]), medianprops=dict(color='black'))
                ax.boxplot(scan_data[1], showmeans=False,
                           positions=[position2], patch_artist=True, widths=0.2, showfliers=False, boxprops=dict(facecolor=colors[1]), medianprops=dict(color='black'))

            ax.set_ylabel(param[param_index])
            for tick in ax.get_xticklabels():
                tick.set_rotation(self.xlabel_angle.get())

            # Set the x-axis tick positions and labels
            ax.set_xticks(group_positions + 0.125)
            ax.set_xticklabels(group_labels)
            ax.set_ylim(0)
            ax.tick_params(axis='both', direction='in')

            # Set the common legend for subgroups
            legend_labels = subgroup_labels
            handles = [plt.Rectangle((0, 0), 1, 1, facecolor=colors[i])
                       for i in range(len(colors))]
            # Adjust the top margin to make space for the legend
            self.fig.subplots_adjust(top=0.85)
            legend = self.fig.legend(handles, legend_labels, loc='upper center', ncol=len(subgroup_labels),
                                     bbox_to_anchor=(0.5, 1), bbox_transform=self.fig.transFigure, fancybox=True)

            for label in legend.get_texts():
                label.set_fontsize(13)  # Adjust the font size as desired

        # Adjust the plot layout
        # Adjust the bottom margin to accommodate the legend
        self.fig.tight_layout(rect=[0, 0, 1, 0.95])

        if self.apply_changes_to_y_values_executed:
            # defined in the yvalues and apply function
            print(self.apply_changes_to_y_values)
            self.axes[0].set_ylim(kwargs.get('pce_ymin'),
                                  kwargs.get('pce_ymax'))
            self.axes[1].set_ylim(kwargs.get('jsc_ymin'),
                                  kwargs.get('jsc_ymax'))
            self.axes[2].set_ylim(kwargs.get('voc_ymin'),
                                  kwargs.get('voc_ymax'))
            self.axes[3].set_ylim(kwargs.get('ff_ymin'), kwargs.get('ff_ymax'))
            self.apply_changes_to_y_values_executed = False

        global canvas
        try:
            canvas.get_tk_widget().grid_remove()

        except:
            pass

        canvas = FigureCanvasTkAgg(self.fig, master=self.box_plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)

        # setting the stause of the the latest function executed
        self.plot_together_executed = True
        self.plot_it_executed = False

    def export_data(self):
        try:

            location = filedialog.askdirectory()
            self.DF.to_csv(rf'{location}' + '/summary.csv',
                           index=None, header=True)

        except:
            pass

    def save_graph(self):
        # Prompt the user to choose a save location
        # self.grab_set()
        # self.focus_force()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        global canvas
        if file_path:
            try:
                # Save the graph as an image file
                canvas.figure.savefig(file_path)

            except Exception as e:
                messagebox.showerror(
                    "Save Error", f"An error occurred while saving the graph: {e}")

    def save_graph_together(self):
        # Prompt the user to choose a save location
        # self.grab_set()
        # self.focus_force()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        global canvas_together
        if file_path:
            try:
                # Save the graph as an image file
                canvas_together.figure.savefig(file_path)

            except Exception as e:
                messagebox.showerror(
                    "Save Error", f"An error occurred while saving the graph: {e}")

    def y_values_range(self):  # for plot together function
        self.y_values = tk.Toplevel()
        self.y_values.configure(bg='white')
        self.y_values.title('Set Y-Axis Values')
        tk.Label(self.y_values, text='Y-lim ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=0, column=0, padx=10, pady=5, sticky='w')

        tk.Label(self.y_values, text='PCE ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.y_values, text='Jsc ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=2, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.y_values, text='Voc ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=3, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.y_values, text='FF ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=4, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.y_values, text='Series Resistance ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=5, column=0, padx=10, pady=5, sticky='w')
        tk.Label(self.y_values, text='Shunt Resistance ', font=('calibri 15'), bg='white',
                 fg='#28486B').grid(row=6, column=0, padx=10, pady=5, sticky='w')
        CustomButton(self.y_values, text='Apply', command=self.apply_changes_to_y_values, width=10).grid(row=7, column=0,
                                                                                                         columnspan=3)

        self.pce_ymin_var = tk.IntVar()
        self.pce_ymin = ttk.Combobox(
            self.y_values, textvariable=self.pce_ymin_var)
        self.pce_ymin.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.pce_ymin.config(font=('calibri', (12)), width=5)

        self.pce_ymax_var = tk.IntVar()
        self.pce_ymax = ttk.Combobox(
            self.y_values, textvariable=self.pce_ymax_var)
        self.pce_ymax.grid(row=1, column=2, padx=10, pady=5, sticky='w')
        self.pce_ymax.config(font=('calibri', (12)), width=5)

        self.jsc_ymin_var = tk.IntVar()
        self.jsc_ymin = ttk.Combobox(
            self.y_values, textvariable=self.jsc_ymin_var)
        self.jsc_ymin.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        self.jsc_ymin.config(font=('calibri', (12)), width=5)

        self.jsc_ymax_var = tk.IntVar()
        self.jsc_ymax = ttk.Combobox(
            self.y_values, textvariable=self.jsc_ymax_var)
        self.jsc_ymax.grid(row=2, column=2, padx=10, pady=5, sticky='w')
        self.jsc_ymax.config(font=('calibri', (12)), width=5)

        self.voc_ymin_var = tk.IntVar()
        self.voc_ymin = ttk.Combobox(
            self.y_values, textvariable=self.voc_ymin_var)
        self.voc_ymin.grid(row=3, column=1, padx=10, pady=5, sticky='w')
        self.voc_ymin.config(font=('calibri', (12)), width=5)

        self.voc_ymax_var = tk.IntVar()
        self.voc_ymax = ttk.Combobox(
            self.y_values, textvariable=self.voc_ymax_var)
        self.voc_ymax.grid(row=3, column=2, padx=10, pady=5, sticky='w')
        self.voc_ymax.config(font=('calibri', (12)), width=5)

        self.ff_ymin_var = tk.IntVar()
        self.ff_ymin = ttk.Combobox(
            self.y_values, textvariable=self.ff_ymin_var)
        self.ff_ymin.grid(row=4, column=1, padx=10, pady=5, sticky='w')
        self.ff_ymin.config(font=('calibri', (12)), width=5)

        self.ff_ymax_var = tk.IntVar()
        self.ff_ymax = ttk.Combobox(
            self.y_values, textvariable=self.ff_ymax_var)
        self.ff_ymax.grid(row=4, column=2, padx=10, pady=5, sticky='w')
        self.ff_ymax.config(font=('calibri', (12)), width=5)

        self.series_ymin_var = tk.IntVar()
        self.series_ymin = ttk.Combobox(
            self.y_values, textvariable=self.series_ymin_var)
        self.series_ymin.grid(row=5, column=1, padx=10, pady=5, sticky='w')
        self.series_ymin.config(font=('calibri', (12)), width=5)

        self.series_ymax_var = tk.IntVar()
        self.series_ymax = ttk.Combobox(
            self.y_values, textvariable=self.series_ymax_var)
        self.series_ymax.grid(row=5, column=2, padx=10, pady=5, sticky='w')
        self.series_ymax.config(font=('calibri', (12)), width=5)

        self.shunt_ymin_var = tk.IntVar()
        self.shunt_ymin = ttk.Combobox(
            self.y_values, textvariable=self.shunt_ymin_var)
        self.shunt_ymin.grid(row=6, column=1, padx=10, pady=5, sticky='w')
        self.shunt_ymin.config(font=('calibri', (12)), width=5)

        self.shunt_ymax_var = tk.IntVar()
        self.shunt_ymax = ttk.Combobox(
            self.y_values, textvariable=self.shunt_ymax_var)
        self.shunt_ymax.grid(row=6, column=2, padx=10, pady=5, sticky='w')
        self.shunt_ymax.config(font=('calibri', (12)), width=5)

        if self.plot_together_executed:
            self.pce_ymin.set(self.axes[0].get_ylim()[0])
            self.pce_ymax.set(self.axes[0].get_ylim()[1])
            self.jsc_ymin.set(self.axes[1].get_ylim()[0])
            self.jsc_ymax.set(self.axes[1].get_ylim()[1])
            self.voc_ymin.set(self.axes[2].get_ylim()[0])
            self.voc_ymax.set(self.axes[2].get_ylim()[1])
            self.ff_ymin.set(self.axes[3].get_ylim()[0])
            self.ff_ymax.set(self.axes[3].get_ylim()[1])
        elif self.plot_it_executed:
            if self.parameter.get() == 'PCE':
                self.pce_ymin.set(self.axes.get_ylim()[0])
                self.pce_ymax.set(self.axes.get_ylim()[1])

            elif self.parameter.get() == 'Jsc':
                self.jsc_ymin.set(self.axes.get_ylim()[0])
                self.jsc_ymax.set(self.axes.get_ylim()[1])

            elif self.parameter.get() == 'Voc':
                self.voc_ymin.set(self.axes.get_ylim()[0])
                self.voc_ymax.set(self.axes.get_ylim()[1])

            elif self.parameter.get() == 'FF':
                self.ff_ymin.set(self.axes.get_ylim()[0])
                self.ff_ymax.set(self.axes.get_ylim()[1])

            elif self.parameter.get() == 'Series':
                self.series_ymin.set(self.axes.get_ylim()[0])
                self.series_ymax.set(self.axes.get_ylim()[1])

            elif self.parameter.get() == 'Shunt':
                self.shunt_ymin.set(self.axes.get_ylim()[0])
                self.shunt_ymax.set(self.axes.get_ylim()[1])

        # else:
        #     messagebox.showinfo(title='Error!', message='Please plot the graph first')

        self.y_values.mainloop()

    def apply_changes_to_y_values(self):  # for y values

        if self.plot_together_executed:
            self.apply_changes_to_y_values_executed = True
            self.plot_together(color1='lightblue', color2='lightgreen',
                               pce_ymin=self.pce_ymin_var.get(), pce_ymax=self.pce_ymax_var.get(),
                               jsc_ymin=self.jsc_ymin_var.get(), jsc_ymax=self.jsc_ymax_var.get(),
                               voc_ymin=self.voc_ymin_var.get(), voc_ymax=self.voc_ymax_var.get(),
                               ff_ymin=self.ff_ymin_var.get(), ff_ymax=self.ff_ymax_var.get())
            # setting the status pf apply back to False
            self.apply_changes_to_y_values_executed = False
            self.y_values.destroy()
        elif self.plot_it_executed:
            self.apply_changes_to_y_values_executed = True
            self.plot_it(pce_ymin=self.pce_ymin_var.get(), pce_ymax=self.pce_ymax_var.get(),
                         jsc_ymin=self.jsc_ymin_var.get(), jsc_ymax=self.jsc_ymax_var.get(),
                         voc_ymin=self.voc_ymin_var.get(), voc_ymax=self.voc_ymax_var.get(),
                         ff_ymin=self.ff_ymin_var.get(), ff_ymax=self.ff_ymax_var.get(),
                         series_ymin=self.shunt_ymin_var.get(), series_ymax=self.series_ymax_var.get(),
                         shunt_ymin=self.shunt_ymin_var.get(), shunt_ymax=self.shunt_ymax_var.get())
            # setting the status pf apply back to False
            self.apply_changes_to_y_values_executed = False
            self.y_values.destroy()


class DataPlot(tk.Toplevel):
    def __init__(self, address):
        super().__init__()
        screen_width = self.winfo_screenwidth()
        screen_width = int(0.8 * screen_width)
        screen_height = self.winfo_screenheight()
        screen_height = int(0.65 * screen_height)
        self.geometry(f'{screen_width}x{screen_height}+100+100')
        self.minsize(1300, 750)
        self.configure(bg='white')

        self.wm_title('PlotIT 3.0')
        self.iconbitmap(r'icon.ico')

        notebook = ttk.Notebook(self)

        boxplot = BoxPlot(notebook, address)
        notebook.add(boxplot, text="Box Plot")

        jv = JV(notebook, address)
        notebook.add(jv, text="JV")

        notebook.pack(fill='both', expand=True)

# if __name__ == "__main__":
#     main_dir = ['C:\\Users\\pcgre\\OneDrive - Swansea University\\Projects\\Python\\PlotIT_latest/users/Rahul Patidar/Batch BP02\\S00 CONTROL 1MG-ML PTAA ACN 110C 10MINS', 'C:\\Users\\pcgre\\OneDrive - Swansea University\\Projects\\Python\\PlotIT_latest/users/Rahul Patidar/Batch BP02\\S01 1MG-ML PTAA ACN 120C 10MINS', 'C:\\Users\\pcgre\\OneDrive - Swansea University\\Projects\\Python\\PlotIT_latest/users/Rahul Patidar/Batch BP02\\S02 1MG-ML PTAA ACN 130C 10MINS', 'C:\\Users\\pcgre\\OneDrive - Swansea University\\Projects\\Python\\PlotIT_latest/users/Rahul Patidar/Batch BP02\\S03 1MG-ML PTAA ACN 110C 10MINS 20MG_ML PCBM', 'C:\\Users\\pcgre\\OneDrive - Swansea University\\Projects\\Python\\PlotIT_latest/users/Rahul Patidar/Batch BP02\\S04 1MG-ML ONE STEP PTAA ACN 110C 10MINS']
#     app = DataPlot(address=main_dir)
