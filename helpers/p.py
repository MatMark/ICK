# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |


import numpy as np


class PWave():
    def __init__(self):
        pass

    # finding P wave in ECG signal
    def find_p(self, ecg, r_x):
        self.p_x, self.p_y = [], []
        for i in range(len(r_x) - 1):
            fragment = ecg[r_x[i]:r_x[i+1]]
            self.minimal_value, self.avg_value = self.find_minimal_value_and_avg(
                fragment)
            # remove elements if above average value and next 3 elements (to the left) are not bigger
            while (len(fragment) > 1 and fragment[-1] > (self.avg_value)):
                if(fragment[-1] < fragment[-2] and fragment[-1] < fragment[-3] and fragment[-1] < fragment[-4]):
                    break
                fragment = fragment[:-1:]
            # get only right half of R-R interval
            right_half = fragment[int(fragment.size*2/3)::]
            # P must be 20% above average value
            above_minimum = list(
                filter(self.check_is_above_minimal, right_half))
            if (above_minimum):
                p_y = max(above_minimum)
                p_x = list(right_half).index(p_y) + \
                    int(fragment.size*2/3) + r_x[i]
                self.p_x.append(p_x)
                self.p_y.append(p_y)
        return self.p_x, self.p_y

    def check_is_above_minimal(self, number):
        if number >= self.minimal_value:
            return True
        return False

    def find_minimal_value_and_avg(self, fragment):
        temp = np.sort(fragment)
        # remove max 10
        temp = temp[10::]
        # remove min 10
        temp = temp[:-10:]
        if temp.size > 0:
            avg = np.mean(temp)
            return avg+abs(avg*.2), avg
        return 0, 0
