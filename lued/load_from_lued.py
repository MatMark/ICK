import wfdb
import numpy as np
record = wfdb.rdsamp('lued/1', sampto=3000)
print(record)
# annotation = wfdb.rdann('mitdb/1', 'atr', sampto=3000)
num = int(record[0].size / 2)
print(num)
result = np.empty(shape=[0])
# for x in range(0, num):
#     result = np.append(result, record[0][x][0])
# np.savetxt("1.csv", result, delimiter=",")
print(result)
