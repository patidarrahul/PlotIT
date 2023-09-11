import numpy as np
import pandas as pd


import glob

def voc_finder(v,j): #for JV scans where x is voltage points and y is current points
     positive_values = []
     negative_values = []
     for i in j:
         if i >= 0:
             positive_values.append(i)
         else:
             negative_values.append(i)
     j1 = min(positive_values)
     j2 = max(negative_values)
     v1 = v[np.where(j == j1)]

     v2 = v[np.where(j == j2)]


     m = (j2 - j1) / (v2 - v1)
     voc = v1 - (j1 / m)  # equation of a line with two points(x1,y1) and (x2,y2) and the value of Voc at Y = 0
     return voc












def find_word(file,column_number, row_number): # to find a word with at a given row and column
    with open(file) as file:
        column = []
        for line in file: #reading a file
            line = line.split()
            if len(line)> column_number: # making sure if the said coloumn number exist
                column.append(line[column_number])#writiing the enitre column into a seperate list
    return column[row_number] # geeting the row number from the column

def index_close_to_zero(list): # designed to find voc but dont work lot of times and hence voc finder was designed
    abs_list = np.array([abs(i) for i in list])
    close_to_zero = min(abs_list)
    return np.where(abs_list == close_to_zero)

def dataframe(dir):

    files = glob.glob(f'{dir}/*.SEQ')
    cell_id = []
    pce_rev = []
    pce_fwd = []
    jsc_rev = []
    jsc_fwd = []
    voc_rev = []
    voc_fwd = []
    ff_rev = []
    ff_fwd = []
    series_rev =[]
    series_fwd = []

    shunt_rev = []
    shunt_fwd =[]
    file_name_dark = []


    for file in files:
        with open(file) as file:
            split_file = []
            for line in file:
                line = line.split('\t')
                split_file.append(line)

            if split_file[28][3] == 'Light':  ##filtering the light current
                cell_id.append(split_file[23][1])

                jsc_rev.append(float(split_file[28][7]))
                jsc_fwd.append(float(split_file[29][7]))

                voc_rev.append(float(split_file[28][5]))
                voc_fwd.append(float(split_file[29][5]))

                ff_rev.append(float(split_file[28][8]))
                ff_fwd.append(float(split_file[29][8]))

                pce_rev.append(float(split_file[28][9]))
                pce_fwd.append(float(split_file[29][9]))

                series_rev.append(split_file[28][15])
                series_fwd.append(split_file[29][15])

                shunt_rev.append(abs(float(split_file[28][14])))
                shunt_fwd.append(abs(float(split_file[29][14])))

    df = pd.DataFrame(list(zip(cell_id, jsc_rev, jsc_fwd, voc_rev, voc_fwd, ff_rev, ff_fwd, pce_rev, pce_fwd, series_rev,series_fwd,shunt_rev,shunt_fwd)),
                      columns=['Cell ID', 'Jsc Rev', 'Jsc Fwd', 'Voc Rev', 'Voc Fwd', 'FF Rev', 'FF Fwd', 'PCE Rev',
                               'PCE Fwd','Series Resistance Rev','Series Resistance Fwd','Shunt Resistance Rev', 'Shunt Resistance Fwd'])

    # for file in files:
    #     try:
    #         data = np.genfromtxt(file, skip_header=10, dtype=float, delimiter='\t')  # loading txt file
    #         voltage_points = data[:, 0]
    #         current_points = data[:, 1]
    #         power_points = current_points * voltage_points
    #         power_max = np.amax(power_points)
    #         max_voltage = np.amax(voltage_points)
    #         voltage_points_rev = []
    #         voltage_points_fwd = []
    #         current_points_fwd = []
    #         current_points_rev = []
    #         current_points_dark = []
    #         voltage_points_dark = []
    #
    #         if power_max <= 10**(-2):  # filtering dark current
    #             current_points_dark = current_points
    #             voltage_points_dark = voltage_points
    #             file_name_dark.append(file[4:-3] + '_dark')
    #         elif voltage_points[
    #             0] == max_voltage and power_max > 10**(-2):  # since dark current is also rev scan extra condition is added
    #             voltage_points_rev = voltage_points
    #             current_points_rev = current_points
    #
    #             power_max = round(power_max, 2)
    #
    #             voc = voc_finder(voltage_points_rev, current_points_rev)
    #             voc = round(voc[0], 2)
    #
    #             jsc = current_points_rev[np.where(voltage_points_rev == 0)]
    #             jsc = round(jsc[0], 2)
    #
    #             ff = 100 * power_max / (voc * jsc)
    #             ff = round(ff, 2)
    #             if voc>0.35 and 15 < ff < 90 and 2 <jsc< 26:##to remove all the bad data
    #                 ##appending the data
    #                 jsc_rev.append(jsc)
    #                 ff_rev.append(ff)
    #                 file_name_rev.append(file)
    #                 voc_rev.append(voc)
    #                 pce_rev.append(power_max)  # storing rv scans pce into a list
    #
    #
    #
    #         else:
    #             voltage_points_fwd = voltage_points
    #             current_points_fwd = current_points
    #             voc = voc_finder(voltage_points_fwd, current_points_fwd)
    #
    #             voc = round(voc[0], 2)
    #
    #             jsc = current_points_fwd[np.where(voltage_points_fwd == 0)]
    #             jsc = round(jsc[0], 2)
    #
    #             ff = 100 * power_max / (voc * jsc)
    #             ff = round(ff, 2)
    #
    #             power_max = round(power_max, 2)
    #
    #             if voc > 0.35 and 15 < ff < 90 and 2 < jsc < 26: ##to remove all the bad data
    #                 pce_fwd.append(power_max)  # storing fwd scans pce into a list
    #                 file_name_fwd.append(file)
    #                 voc_fwd.append(voc)
    #                 ff_fwd.append(ff)
    #                 jsc_fwd.append(jsc)
    #     except:
    #         messagebox.showinfo(message=f'Problem with file {cut_string(file,"/")}\nThis data will not be plotted')




    # storing the entire data in a data frame
    # df = pd.DataFrame(list(zip(file_name_rev, file_name_fwd, jsc_rev, jsc_fwd, voc_rev, voc_fwd, ff_rev, ff_fwd, pce_rev, pce_fwd)),
    #                   columns=['Filename Reverse','Filename Forward', 'Jsc Rev', 'Jsc Fwd', 'Voc Rev', 'Voc Fwd', 'FF Rev', 'FF Fwd', 'PCE Rev',
    #                            'PCE Fwd'])
    return df

def cut_string(string, charac): # cuts the string from behind till the mentioned character
    list_of_indices = [i for i, ltr in enumerate(string) if ltr == charac]
    max_index = max(list_of_indices)
    return string[max_index+1:]

def adjust_lightness(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def get_directories():
    import wx
    import os
    import wx.lib.agw.multidirdialog as MDD
    app = wx.App(0)

    dlg = MDD.MultiDirDialog(None, title="Custom MultiDirDialog", defaultPath=os.getcwd(),
                             agwStyle=MDD.DD_MULTIPLE | MDD.DD_DIR_MUST_EXIST)

    if dlg.ShowModal() != wx.ID_OK:
        dlg.Destroy()
        return

    paths = dlg.GetPaths()
    return paths


    dlg.Destroy()

    app.MainLoop()




