from helpers.load import load_data
from helpers.plotting import plot
from helpers.r import find_r

ecg, fs, file_name = load_data()
r_x, r_y = find_r(ecg)
plot(ecg, fs, file_name, r_x, r_y)
