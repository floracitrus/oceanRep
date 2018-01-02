import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

a = [1,2,3,4]
b = np.roll(a, 1)
c = np.roll(a, -1)

print(a)
print(b)
print(c)

with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	E_Core = list(file['E_Core'])
	P_Core = list(file['P_Core'])
	R_Core = list(file['R_Core'])
	E_Core = np.squeeze(E_Core)
	P_Core = np.squeeze(P_Core)
	R_Core = np.squeeze(R_Core)


	print(E_Core)
	print(P_Core)
	print(R_Core)