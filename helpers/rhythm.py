# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |

import numpy as np


def is_regular_rhythm(rx):
    # copy of the original x coordinates for the R waves
    r_x = rx.copy()

    # removes any excess R waves
    min_dist_between_waves = 20
    i = 0
    while i < (len(r_x) - 1):
        if (r_x[i+1] - r_x[i]) < min_dist_between_waves:
            r_x.remove(r_x[i+1])
            i = i - 1
        i = i + 1

    # list contains differences between the R waves
    new_r_x = []
    i = 0
    while i < (len(r_x) - 1):
        new_r_x.append(r_x[i+1] - r_x[i])
        i = i + 1

    # determination of the standard deviation for differences between the R waves
    min_standard_deviation = 25
    std_dev = np.std(new_r_x)
    if std_dev < min_standard_deviation:
        return True
    else:
        return False
