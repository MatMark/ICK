import math

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def plot(ecg, fs, file_name, r_x, r_y):
    time = np.arange(ecg.size) / fs
    r_x = [x / fs for x in r_x]
    min_var = math.floor(min(ecg))
    max_var = math.ceil(max(ecg))
    height = int(math.dist([min_var], [max_var]))
    width = height*1.25
    fig, ax = plt.subplots(num=None, figsize=(24, 8), dpi=80)
    fig.canvas.manager.set_window_title(file_name)
    ax.plot(time, ecg, color='black', linewidth=.5)
    ax.plot(r_x, r_y, color='blue',
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
    plt.title(file_name + " (przesuw 25mm/s)", fontsize=24)
    plt.xlabel("s", fontsize="20")
    plt.ylabel("mV", fontsize="20")
    plt.xlim(0, width)
    plt.ylim(min_var, max_var)
    plt.show()
