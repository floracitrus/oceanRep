import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math
def maskMatrix(matrix, rangeA, rangeB):
	np.errstate(invalid='ignore')
	m = (matrix>rangeA) & (matrix<rangeB) 
	return m

with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	xxt = list(file['xt']) #360
	yyt = list(file['yt']) #180
	ssa = list(file['SA']) #12x101x180x360
	
	
	#then till 2000 becomes 100 step and last one is 5500
	aaxy = list(file['Axy']) #101x180x360
	
	
	vol = list(file['vol'])
	dx = list(file['dx'])
	dy = list(file['dy'])
	dz = list(file['dz'])

	E_Core = list(file['E_Core'])
	P_Core = list(file['P_Core'])
	R_Core = list(file['R_Core'])
	

	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	zt = np.squeeze(zzt)

	sa  = np.squeeze(ssa)
	axy = np.squeeze(aaxy)
	vol = np.squeeze(vol)
	
	dx = np.squeeze(dx)
	dy = np.squeeze(dy)
	dz = np.squeeze(dz)

	E_Core = np.squeeze(E_Core)
	P_Core = np.squeeze(P_Core)
	R_Core = np.squeeze(R_Core)
	


	RANA = 35.9
	RANB = 36.1
	littled = 5 #1/0.2
	MON = 0
	gridx, gridy = np.meshgrid(xt,yt)

	asf = np.add(E_Core,P_Core)
	asf = np.add(asf, -R_Core)
	ss = np.squeeze(sa[:,0,:,:])
	fs = np.multiply(asf,ss)
	saxy = np.squeeze(axy[0,:,:])
	f = []
	for MON in range(12):
		term = np.multiply(fs[MON, :, :],saxy)
		mask = maskMatrix(np.squeeze(sa[MON,0,:,:]),RANA,RANB)
		mask = mask & ((gridx<280) & (gridx>200))
		c = mask & (gridy<(-5))
		#print(vol[m])
		su = sum(term[c])
		su = su*littled
		su = su/1000000
		f.append(su)

	plt.plot(f)
	plt.show()



