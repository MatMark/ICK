import wfdb
import numpy as np
record = wfdb.rdsamp('mitdb/100', sampto=3000)
annotation = wfdb.rdann('mitdb/100', 'atr', sampto=3000)
num = int(record[0].size / 2)
result = np.empty(shape=[0])
for x in range(0, num):
    result = np.append(result, record[0][x][0])
np.savetxt("100.csv", result, delimiter=",")