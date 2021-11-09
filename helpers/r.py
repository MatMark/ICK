def find_r(ecg):
    r_x, r_y = firstSearch(ecg, findMaximum(ecg))
    return r_x, r_y


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


def findMaximum(ecg):
    maximum = 0
    for i in ecg:
        if(maximum < i):
            maximum = i
    return maximum


def firstSearch(data, max):
    r_x, r_y = [], []
    for i in range(len(data)):
        if(data[i] > (max/2) and checkLeft(data, i) and checkRight(data, i)):
            r_x.append(i)
            r_y.append(data[i])
    return r_x, r_y
