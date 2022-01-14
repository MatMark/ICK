# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |


import numpy as np


def find_base(ecg):
    # signal quantization
    result = list(map(round_dot_one, ecg))
    # find dominant
    vals, counts = np.unique(result, return_counts=True)
    index = np.argmax(counts)
    return vals[index]


def round_dot_one(n):
    return round(n, 1)
