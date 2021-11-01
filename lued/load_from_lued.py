import wfdb
import numpy as np
import os


def load_from_file(path: str = None):
    hea = open(f"{os.path.splitext(path)[0]}.hea", "r")
    hea_text = hea.readline()
    fs = int(hea_text.split()[2])
    num = fs*10
    file_name = os.path.splitext(path)[0]

    record = wfdb.rdsamp(file_name, sampto=num)
    # zawsze tylko dane z pierwszego odprowadzenia
    result = np.empty(shape=[0])
    for x in range(0, num):
        result = np.append(result, record[0][x][0])
    return result, fs
