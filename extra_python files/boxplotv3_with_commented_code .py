
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from Functions import *
from custom_widget import CustomEntry, CustomButton, ScrollableFrame

from matplotlib.patches import Patch
import seaborn as sns
class BoxPlotV3(tk.Toplevel):
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

        self.box_plot = ScrollableFrame(self)
        self.box_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.box_plot.configure(bg='white')
        self.wm_title('PlotIT 3.0')
        self.iconbitmap(r'icon.ico')


        ##customize_column
        customize = tk.Frame(self.box_plot, bg='white', relief='solid', borderwidth=1)
        customize.place(relx=0, rely=0.75, relwidth=1, relheight=1)


        tk.Label(customize, text='Scan:', font=('calibri 13'), bg='white', fg='#28486B').place(x=14, y=10)

        self.scan_choice = tk.StringVar()
        self.scan_choice = ttk.Combobox(customize, textvariable=self.scan_choice,
                                        values=['Reverse', 'Forward', 'Together'], state='readonly')
        self.scan_choice.place(x=100, y=14)
        self.scan_choice.config(font=('calibri', (10)), width=8)
        self.scan_choice.set('Reverse')

        self.optionlist = {'PCE': 'Power Conversion Efficiency (%)', 'Jsc': 'Current Density (mA/cm$^2$)',
                           'FF': 'Fill Factor (%)', 'Voc': 'Open Circuit Voltage (Volts)', 'Series': 'Series Resitance (\u03A9)', 'Shunt': 'Shunt Resitance (\u03A9)'}
        tk.Label(customize, text='Y-axis:', font=('calibri 12'), bg='white', fg='#28486B').place(x=14, y=54)

        self.parameter_var = tk.StringVar()

        self.parameter = ttk.Combobox(customize, textvariable=self.parameter_var, values=['PCE', 'Jsc', 'FF', 'Voc', 'Series', 'Shunt'],
                                      state='readonly')
        self.parameter.config(font=('calibri', (10)), width=8)
        self.parameter.place(x=100, y=58)
        self.parameter.set('PCE')

        tk.Label(customize, text='X-Label Rotation:', font=('calibri 13'), bg='white', fg='#28486B').place(x=250, y=10)
        self.xlabel_angle_var = tk.IntVar()
        self.xlabel_angle = ttk.Combobox(customize, textvariable=self.xlabel_angle_var,
                                         values=[0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
        self.xlabel_angle.config(font=('calibri', (10)), width=2)
        self.xlabel_angle.place(x=450, y=14)
        self.xlabel_angle.set(0)

        tk.Label(customize, text='Label Size:', font=('calibri 13 '), bg='white', fg='#28486B').place(x=250, y=50)
        self.label_size_var = tk.IntVar()

        self.label_size = ttk.Combobox(customize, textvariable=self.label_size_var, values=[1, 2, 3, 4, 5, 6, 7, 8, 13])

        self.label_size.config(font=('calibri', (10)), width=2)
        self.label_size.place(x=450, y=54)
        self.label_size.set(5)

        tk.Label(customize, text='Y-lim ', font=('calibri 13'), bg='white',
                 fg='#28486B').place(x=250, y=94)
        self.y_lim_var = tk.IntVar()
        self.y_limit = ttk.Combobox(customize, textvariable=self.y_lim_var)
        self.y_limit.place(x=450, y=94)

        CustomButton(customize, text='Box Plot', command=self.plot_it, width=10, borderwidth=0.5).place(relx=0.01, rely=0.2)
        CustomButton(customize, text='Together', command=self.plot_together, width=10, borderwidth=0.5).place(relx=0.09, rely=0.2)
        save_button = CustomButton(customize, text="Save Graph", command=self.save_graph,width=10, borderwidth=0.5)
        save_button.place(relx=0.17, rely=0.2)

        button_export_data = tk.Button(customize, text='Export Data', font='calibri 14', command=self.export_data,
                                       borderwidth=0,
                                       bg='white', cursor='hand2')
        button_export_data.place(relx=0.88, rely=0.02)

        # Generate a list of colors using cm.rainbow colormap


        self.color_choice_fill = sns.color_palette('pastel')


        self.color_choice_border = sns.color_palette('deep')

        self.entry_list = [cut_string(i, '\\') for i in
                           self.addresses_to_plot]  ##to store all the string variables of entry widget
        self.entry_list_var = []
        self.entry_widget_list = []
        self.auto_entry_generation()
        self.plot_together(color1='lightblue', color2='lightgreen')





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
        tk.Label(self.box_plot, text = 'Labels:',font=('calibri 12'), bg='white', fg='#28486B' ).place(x=1000, y = 50)
        for i in range(len(self.entry_list)):
            self.entry_list_var.append([''])  ##just a dummy place for it change in the next line
            self.entry_list_var[i] = tk.StringVar(self)
            e = CustomEntry(self.box_plot, width=20, textvariable=self.entry_list_var[i])
            e.place(x=1000, y=80 + 40 * i, height=30)
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
                    lst = [int(float(i)) for i in lst]
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
                    lst = [int(float(i)) for i in lst]
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


        ## plotting both scans in single graph

        f, ax = plt.subplots(figsize=(4.5, 2.8), dpi = 150)

        if self.scan_choice.get() == 'Together':

            ax.set_ylabel(self.optionlist[self.parameter.get()], fontsize=7)
            ax.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')
            if self.y_lim_var.get() != 0:
                ax.set_ylim(0, self.y_lim_var.get())
            for tick in ax.get_xticklabels():
                tick.set_rotation(self.xlabel_angle.get())

            #plotting data_rev
            for i, scan_data_rev in enumerate(data_rev):
                ax.boxplot(scan_data_rev, showmeans=False, positions=[i],
                                 widths=0.2
                           , showfliers=False,
                           boxprops=dict(color=self.color_choice_border[i]),
                           medianprops=dict(color=self.color_choice_border[i]),
                           whiskerprops=dict(color=self.color_choice_border[i]),
                           capprops=dict(color=self.color_choice_border[i]))
             #adding jitters
            for i in range(self.total_splits):
                x_axis = np.random.normal(i, 0.05, size=len(data_fwd[i]))
                ax.plot(x_axis, data_rev[i], color=self.color_choice_border[i], marker='o', linestyle='none', ms=2,
                        label=self.label_list)

            # plotting data_fwd
            for i, scan_data_fwd in enumerate(data_fwd):
                ax.boxplot(scan_data_fwd, showmeans=False, positions=[i+0.3],
                           patch_artist=True, widths=0.2
                           , showfliers=False,
                           boxprops=dict(facecolor=self.color_choice_fill[i], color=self.color_choice_border[i]),
                           medianprops=dict(color=self.color_choice_border[i]),
                           whiskerprops=dict(color=self.color_choice_border[i]),
                           capprops=dict(color=self.color_choice_border[i]))
            # adding jitters
            for i in range(self.total_splits):
                x_axis = np.random.normal(i+0.3, 0.05, size=len(data_fwd[i]))
                ax.plot(x_axis, data_fwd[i], color=self.color_choice_border[i], marker='o', linestyle='none', ms=2,
                        label=self.label_list)

            group_labels = []
            for i in range(len(self.entry_list_var)):
                group_labels.append(self.entry_list_var[i].get())

            ax.set_xticks([i + 0.15 for i in range(self.total_splits)])
            ax.set_xticklabels(group_labels)


            legend_handles = [Patch(facecolor='none', edgecolor='lightgrey', label='Reverse Scan'),
                              Patch(facecolor='lightgrey', edgecolor='lightgrey', label='Forward Scan')]
            f.subplots_adjust(top=0.92)  # Adjust the top margin to make space for the legend
            #f.legend(legend_handles,  loc='upper center', ncol=len(legend_labels),
            #           bbox_to_anchor=(0.5, 1), bbox_transform=f.transFigure, fancybox=True, shadow=True)
            f.legend(handles = legend_handles, loc='upper center',ncol =2, fontsize = '6', frameon =False)

        else:

            ax.set_ylabel(self.optionlist[self.parameter.get()], fontsize=7)
            ax.tick_params(axis='both', which='major', labelsize=self.label_size.get(), direction='in')
            if self.y_lim_var.get() != 0:
                ax.set_ylim(0, self.y_lim_var.get())
            for tick in ax.get_xticklabels():
                tick.set_rotation(self.xlabel_angle.get())
            #ax.boxplot(data, meanline=True, labels=self.label_list, showfliers=False)
            for i, scan in enumerate(data):
                box1 = ax.boxplot(scan, showmeans=False,positions =[i],
                                  patch_artist=True, widths=0.2
                                  , showfliers=False, boxprops=dict(facecolor=self.color_choice_fill[i], color = self.color_choice_border[i]),
                                  medianprops=dict(color=self.color_choice_border[i]), whiskerprops=dict(color=self.color_choice_border[i]),
                          capprops=dict(color=self.color_choice_border[i]))


            for i in range(self.total_splits):
                x_axis = np.random.normal(i, 0.05, size=len(data[i]))
                ax.plot(x_axis, data[i], color  = self.color_choice_border[i], marker = 'o', linestyle='none', ms=2,label = self.label_list )

            group_labels = []
            for i in range(len(self.entry_list_var)):
                group_labels.append(self.entry_list_var[i].get())

            ax.set_xticks([i + 0.15 for i in range(self.total_splits)])
            ax.set_xticklabels(group_labels)
        global canvas
        try:
            canvas.get_tk_widget().place_forget()

        except:
            pass
        ax.tick_params(axis='x', length=0)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=0)


    def plot_together(self, color1='lightblue', color2='lightgreen'):
        # Generate sample data
        dataf = self.DF
        num_groups = int(len(dataf.columns) / 13)  # 13 is the number of columns per data set
        data_pce = []
        data_jsc = []
        data_voc = []
        data_ff = []

        param = ['Power Conversion Efficiency (%)', 'Current Density $(mAcm^{-2})$', 'Open Circuit Voltage (Voc)',
                 'Fill Factor (%)']
        ##getting rerverse anf forward data from the csv file for each group and for each parameter and appending it into the main list (data_jsc)
        for num_groups_index in range(num_groups):
            index = num_groups_index * 13
            jsc = [(dataf.iloc[:, index + 1]).dropna().tolist(), (dataf.iloc[:, index + 2]).dropna().tolist()]
            data_jsc.append(jsc)
            voc = [(dataf.iloc[:, index + 3]).dropna().tolist(), (dataf.iloc[:, index + 4]).dropna().tolist()]
            data_voc.append(voc)
            ff = [(dataf.iloc[:, index + 5]).dropna().tolist(), (dataf.iloc[:, index + 6]).dropna().tolist()]
            data_ff.append(ff)
            pce = [(dataf.iloc[:, index + 7]).dropna().tolist(), (dataf.iloc[:, index + 8]).dropna().tolist()]
            data_pce.append(pce)
        data = [data_pce, data_jsc, data_voc, data_ff]


        group_labels = []
        for i in range(len(self.entry_list_var)):
           group_labels.append(self.entry_list_var[i].get())

        subgroup_labels = ['Reverese', 'Forward']

        # Create the figure and axes
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9, 5.2), dpi = 80)

        # Flatten the axes array for easier indexing
        axes = axes.flatten()

        # Define the default colors for the boxes
        default_colors = ['lightblue', 'lightgreen']

        # Validate and set user-selected colors
        if color1:
            colors = [color1, color2]
        else:
            colors = default_colors

        # Iterate over the param
        for param_index in range(len(param)):
            ax = axes[param_index]  # Get the corresponding axis

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
                           positions=[position1], patch_artist=True, widths=0.2
                           , showfliers=False, boxprops=dict(facecolor=colors[0]), medianprops=dict(color='black'))
                ax.boxplot(scan_data[1], showmeans=False,
                           positions=[position2], patch_artist=True, widths=0.2
                           , showfliers=False, boxprops=dict(facecolor=colors[1]), medianprops=dict(color='black'))

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
            handles = [plt.Rectangle((0, 0), 1, 1, facecolor=colors[i]) for i in range(len(colors))]
            fig.subplots_adjust(top=0.85)  # Adjust the top margin to make space for the legend
            fig.legend(handles, legend_labels, loc='upper center', ncol=len(subgroup_labels),
                       bbox_to_anchor=(0.5, 1), bbox_transform=fig.transFigure, fancybox=True, shadow=True)

        # Adjust the plot layout
        fig.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust the bottom margin to accommodate the legend

        global canvas

        try:
            canvas.get_tk_widget().place_forget()

        except:
            pass

        canvas = FigureCanvasTkAgg(fig, master = self.box_plot)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=20)

        # Return the figure


    def export_data(self):
        try:

            location = filedialog.askdirectory()
            self.DF.to_csv(rf'{location}' + '/summary.csv', index=None, header=True)

        except:
            pass


    def save_graph(self):
        # Prompt the user to choose a save location
        self.grab_set()
        self.file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        global canvas
        if self.file_path:
            try:
                # Save the graph as an image file
                canvas.figure.savefig(self.file_path)
                #messagebox.showinfo("Save Successful", "Graph saved successfully.")
            except Exception as e:
                messagebox.showerror("Save Error", f"An error occurred while saving the graph: {e}")
        # else:
        #     messagebox.showinfo("Save Cancelled", "Graph save cancelled.")


if __name__ == '__main__':
    root = BoxPlotV3(address)  # Replace 'address' with the desired input address
    root.mainloop()






