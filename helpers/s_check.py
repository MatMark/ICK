# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |

import r as r_methods


def find_s(ecg, baseline):
    negative_ecg = []
    # making opposite ecg signal
    for i in ecg:
        negative_ecg.append(i*(-1))
    s_x, s_y = [], []
    base_value = baseline[0] * (-1)
    # move signal so the baseline is on y=0
    # if the sample is negative then set it as 0
    for j in range(len(negative_ecg)):
        negative_ecg[j] = negative_ecg[j] - base_value
        if negative_ecg[j] < 0:
            negative_ecg[j] = 0
    # search for s using find_r
    s_x, s_y = r_methods.find_r(negative_ecg)
    return s_x, s_y

    
def checkBeforeS(ecg, baseline, fs):
    sus_x, sus_y = [], []
    r_x, r_y = r_methods.find_r(ecg)
    s_x, s_y = find_s(ecg, baseline)
    # number of samples in range of 40 miliseconds
    samples = (fs*4)//100
    for i in range(len(s_x)):
        for j in range(len(r_x)):
            if r_x[j] < s_x[i] and r_x[j] > (s_x[i] - samples):
                sus_x.append(j)
                sus_y.append(r_y[j])
                break
    return sus_x, sus_y

