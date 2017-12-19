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
	m = (matrix>=rangeA) & (matrix<rangeB) 
	return m

with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	xxt = list(file['xt']) #360
	yyt = list(file['yt']) #180
	ssa = list(file['SA']) #12x101x180x360
	zzt = list(file['zt']) #100 first 100 is 5 step, then 25 step, then till 1000 becomes 50 step
	
	#then till 2000 becomes 100 step and last one is 5500
	aaxy = list(file['Axy']) #101x180x360
	aayz = list(file['Ayz']) #101x180x360
	aaxz = list(file['Axz']) #101x180x360
	
	vol = list(file['vol'])
	dx = list(file['dx'])
	dy = list(file['dy'])
	dz = list(file['dz'])
	
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	zt = np.squeeze(zzt)

	sa  = np.squeeze(ssa)
	axy = np.squeeze(aaxy)
	ayz = np.squeeze(aayz)
	vol = np.squeeze(vol)
	
	dx = np.squeeze(dx)
	dy = np.squeeze(dy)
	dz = np.squeeze(dz)

	RANA = 35.9
	RANB = 36.1
	littled = 5 #1/0.1
	MON = 0
	tot = 0
	for k in range(210,280):
	
		saJanSurf = np.squeeze(sa[MON, :, :, k])
		#gridz, gridy = np.meshgrid(zt,yt)

		newM = np.array(saJanSurf)
		for i in range(101):
			for j in range(180):
				if(saJanSurf[i][j]>RANB):
					newM[i][j] = RANB
				elif(saJanSurf[i][j]<RANA):
					newM[i][j] = RANA
				else:
					newM[i][j] = saJanSurf[i][j]

		newzM = np.c_[newM, np.transpose(newM)[0]]  ##add an extra column	
		partialzM = []
		difz = dz[:,:,k]
		difz = np.roll(difz, 1, axis = 1)
		for i in range(101):
			partialzM.append(np.diff(newzM[i]))		
		partialzM = np.multiply(partialzM, 0.00005) #times D 5e-05
		partialzM = np.divide(partialzM, difz)
		


		partialzM = np.c_[partialzM, np.transpose(partialzM)[0]]
		fluxzM = []
		for i in range(101):
			fluxzM.append(np.diff(partialzM[i]))	
		dif3z = dz[:,:,k]
		dif3z = np.roll(dif3z, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
		#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1 #WRONG

		difz = np.add(difz, dif3z) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
		difz = np.multiply(difz, 0.5)#1/2(x3-x1)
		difz = np.array(difz)
		#print(difx.shape())
		fluxzM = np.divide(fluxzM, difz)

		# plt.figure(2)
		# plt.title("salt flux of salinity in z-dir 36(36.1->35.9)")
		# plt.xlabel("latitude")
		# plt.ylabel("depth")
		
		# plt.imshow(fluxzM, extent=[yt.min(), yt.max(), zt.min(), 1500], 
	 #                 interpolation='nearest', origin='lower',cmap = "seismic")
		# plt.gca().invert_yaxis()
		# plt.colorbar()
		sumPos = 0
		sumNeg = 0
		for i in range(101):
			for j in range(180):
				if(np.isnan(fluxzM[i][j])):
					sumPos = sumPos
					sumNeg = sumNeg
				elif(fluxzM[i][j]>0 ):
					sumPos += fluxzM[i][j]
					#print("z positive")
					#print(sumPos)
				elif(fluxzM[i][j]<0):
					sumNeg += fluxzM[i][j]
					#print("z negative")
					#print(sumNeg)
		
		tot += (sumPos*littled+sumNeg*littled) #-3.13289551605e-06 January 36

	print(tot)
	
	# plt.show()





