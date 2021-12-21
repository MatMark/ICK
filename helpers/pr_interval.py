# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |


import numpy as np


class PRInterval:
    def __init__(self):
        pass

    p_absence_amount = 0

    def find_diff(self, r_wave, p_wave):
        global p_absence_amount
        diff_array = []
        for i in range(1, len(r_wave)):
            pom = 0
            for j in range(len(p_wave)):
                if (pom == 0) and (p_wave[j] > r_wave[i - 1]):
                    pom = r_wave[i] - p_wave[j]
                    continue
                if r_wave[i]-p_wave[j] < 0:
                    break
                if (r_wave[i] - p_wave[j] < pom) and (r_wave[i] - p_wave[j] > r_wave[i - 1]):
                    pom = r_wave[i] - p_wave[j]
                    continue
            if r_wave[i] - pom > r_wave[i-1]:
                diff_array.append(pom)
            else:
                self.p_absence_amount = self.p_absence_amount + 1

        print(diff_array)
        return diff_array

    def get_pr_interval(self, rx, px, fs):
        # copy of the original x coordinates for the R waves
        r_x = rx.copy()
        p_x = px.copy()

        mean = np.mean(self.find_diff(r_x, p_x))
        mean_in_seconds = mean / fs
        print(mean_in_seconds)
        if self.p_absence_amount > len(r_x)/4:
            return "nie wykryto załamków P"
        else:
            return mean_in_seconds
