import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import helpers.load_from_mendeley as mendeley
import helpers.load_from_mitdb as mitdb


def load_data():
    Tk().withdraw()
    path = askopenfilename()
    extension = os.path.splitext(path)[1]
    file_name = os.path.basename(path)

    if(extension == '.dat' or extension == '.hea'):
        ecg, fs = mitdb.load_from_file(path=path)
    elif(extension == '.mat'):
        ecg, fs = mendeley.load_from_file(path=path)
    else:
        print('error')
    return ecg, fs, file_name
