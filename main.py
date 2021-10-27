from scipy.misc import electrocardiogram
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

file_name = '12345'

# ecg = electrocardiogram()
import scipy.io
ecg = scipy.io.loadmat('106m (0).mat').get('val')[0]
print(ecg)

fs = 360
time = np.arange(ecg.size) / fs


fig, ax = plt.subplots(num=None, figsize=(32, 16), dpi=80)
fig.canvas.manager.set_window_title(file_name)
ax.plot(time, ecg, color='black', linewidth=.5)
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
