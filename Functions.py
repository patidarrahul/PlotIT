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



