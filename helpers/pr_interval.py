# | Miłosz Dziadosz, Krystian Kania, Mateusz Markowski |
# |             POLITECHNIKA WROCŁAWSKA                |
# |      WYDZIAŁ INFORMATYKI I TELEKOMUNIKACJI         |
# |                    2021/2022                       |


import numpy as np


class PRInterval:
    def __init__(self):
        pass

    # counts all cases where no PR wave was detected
    p_absence_amount = 0

    # designates all PR intervals
    def find_diff(self, r_wave, p_wave):
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

        return diff_array

    # returns the mean value of PR interval
    def get_pr_interval(self, rx, px, fs):
        # copy of the original x coordinates for the R waves
        r_x = rx.copy()

        # copy of the original x coordinates for the P waves
        p_x = px.copy()

        # removes any excess R waves
        min_dist_between_waves = 20
        i = 0
        while i < (len(r_x) - 1):
            if (r_x[i + 1] - r_x[i]) < min_dist_between_waves:
                r_x.remove(r_x[i + 1])
                i = i - 1
            i = i + 1

        # calculates the mean value of all PR intervals
        mean = np.mean(self.find_diff(r_x, p_x))
        mean_in_seconds = mean / fs
        if self.p_absence_amount > len(r_x)/4:
            return -1
        else:
            return mean_in_seconds
