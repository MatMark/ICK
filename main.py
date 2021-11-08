import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import mendeley.load_from_mendeley as mendeley
import mitdb.load_from_mitdb as mitdb


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


def checkLeft(data, position):
    if(position == 0):
        return False
    if(position >= 10):
        for i in range(position-10, position):
            if(data[i] > data[position]):
                return False
    if(position > 0 and position < 10):
        for j in range(0, position):
            if(data[j] > data[position]):
                return False
    return True


def checkRight(data, position):
    if(position == len(data)-1):
        return False
    if(position < len(data)-11):
        for i in range(position+1, position+11):
            if(data[i] > data[position]):
                return False
    if(position > len(data)-10 and position < len(data)-1):
        for j in range(position+1, len(data)):
            if(data[j] > data[position]):
                return False
    return True


def findMaximum(data):
    maximum = 0
    for i in ecg:
        if(maximum < i):
            maximum = i
    return maximum


def firstSearch(data, max):
    zalamki_x, zalamki_y = [], []
    for i in range(len(data)):
        if(data[i] > (max/2) and checkLeft(data, i) and checkRight(data, i)):
            zalamki_x.append(i)
            zalamki_y.append(data[i])
    return zalamki_x, zalamki_y


def plotting(ecg, fs, file_name, zalamki_x, zalamki_y):
    time = np.arange(ecg.size) / fs
    zalamki_x = [x / fs for x in zalamki_x]
    fig, ax = plt.subplots(num=None, figsize=(32, 16), dpi=80)
    fig.canvas.manager.set_window_title(file_name)
    ax.plot(time, ecg, color='black', linewidth=.5)
    ax.plot(zalamki_x, zalamki_y, color='blue',
            marker='o', linewidth=3, linestyle="None")
    plt.grid(axis="x", color="r", alpha=.5, linewidth=.5, which='major')
    plt.grid(axis="y", color="r", alpha=.5, linewidth=.5, which='major')
    plt.grid(axis="x", color="r", alpha=.5, linewidth=.2, which='minor')
    plt.grid(axis="y", color='r', alpha=.5, linewidth=.2, which='minor')
    major_locator_x = ticker.MultipleLocator(base=0.2)
    ax.xaxis.set_major_locator(major_locator_x)
    major_locator_y = ticker.MultipleLocator(base=.5)
    ax.yaxis.set_major_locator(major_locator_y)
    minor_locator_x = ticker.AutoMinorLocator(5)
    minor_locator_y = ticker.AutoMinorLocator(5)
    ax.xaxis.set_minor_locator(minor_locator_x)
    ax.yaxis.set_minor_locator(minor_locator_y)
    plt.tick_params(which='major', length=7, color='r')
    plt.tick_params(which='minor', length=4, color='r')
    for spine in ['top', 'right', 'bottom', 'left']:
        ax.spines[spine].set_color('red')
    plt.title("Sygnał EKG nr " + file_name + " (przesuw 25mm/s)", fontsize=24)
    plt.xlabel("s", fontsize="20")
    plt.ylabel("mV", fontsize="20")
    plt.xlim(0, 4)
    plt.ylim(-3, 3)
    plt.show()


ecg, fs, file_name = load_data()
zalamki_x, zalamki_y = firstSearch(ecg, findMaximum(ecg))
plotting(ecg, fs, file_name, zalamki_x, zalamki_y)
