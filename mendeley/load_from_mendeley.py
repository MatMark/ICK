import scipy.io
mat = scipy.io.loadmat('mendeley/213m (4).mat')
print(mat)
print(mat.get('val')[0])
