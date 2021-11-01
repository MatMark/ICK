import scipy.io


def load_from_file(path: str = None):
    mat = scipy.io.loadmat(path)
    fs = 360
    # przesunięcie o -5 dla wyrównania wykresu
    result = (mat.get('val')[0]/200)-5
    return result, fs
