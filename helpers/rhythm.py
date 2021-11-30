import numpy as np


def is_regular_rhythm(rx):
    r_x = rx.copy()
    i = 0
    while i < (len(r_x) - 1):
        if (r_x[i+1] - r_x[i]) < 20:
            r_x.remove(r_x[i+1])
            i = i - 1
        i = i + 1

    new_r_x = []
    i = 0
    while i < (len(r_x) - 1):
        new_r_x.append(r_x[i+1] - r_x[i])
        i = i + 1
    std_dev = np.std(new_r_x)
    if std_dev < 25:
        return True
    else:
        return False







