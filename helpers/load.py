# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                      2021                          |


import os
from PyQt5.QtWidgets import QFileDialog

import helpers.load_from_mendeley as mendeley
import helpers.load_from_mitdb as mitdb


# loading data from file
def load_data(context):
    # open file explorer
    path = QFileDialog.getOpenFileName(context, 'Open a file', '',
                                       'All Files (*.*)')
    path = path[0]
    extension = os.path.splitext(path)[1]
    file_name = os.path.basename(path)

    # load data with properly loader
    if(extension == '.dat' or extension == '.hea'):
        ecg, fs = mitdb.load_from_file(path=path)
    elif(extension == '.mat'):
        ecg, fs = mendeley.load_from_file(path=path)
    else:
        print('error')
    return ecg, fs, file_name
