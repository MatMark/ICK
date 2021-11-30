# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                      2021                          |


import scipy.io


def load_from_file(path: str = None):
    mat = scipy.io.loadmat(path)
    fs = 360
    result = (mat.get('val')[0]/200)-5
    return result, fs
