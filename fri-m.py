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
	dz = list(file['dz'])
	vol = list(file['vol'])
	sa  = np.squeeze(ssa)
	dz = np.squeeze(dz)
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	vol = np.squeeze(vol)
	
	RANA = 35.9
	RANB = 36.1
	littled = 5
	
	gridx, gridy = np.meshgrid(xt,yt)

	#dz
	dz1 = np.add(dz,np.roll(dz,1, axis = 0))
	dz1 = np.multiply(dz1,0.5)
	
	dz2 = np.add(dz, np.roll(dz, 2, axis = 0))
	dz2 = np.multiply(dz2,0.5)
	

	MON = 0
	mylist = []
	for MON in range(12):

		#每一个mask只对应那个月里面所有圈圈里的方块的坐标和值
		mask = maskMatrix(np.squeeze(sa[MON,:,:,:]),RANA,RANB)
		mask = mask & ((gridx<280) & (gridx>200))
		c = mask & (gridy<(-5))
		#c取到了这个圈圈馁的所有的点

		salinity = np.squeeze(sa[MON, :, :, :])
		
		partialzM = np.diff(salinity,axis=0)
		shape = (180,360)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		partialzM = np.append(partialzM,[np.ones(shape)],axis=0)
		partialzM = np.divide(partialzM, dz1)
		partialzM = np.multiply(partialzM, 0.00005) 
		#因为知道最后两行没关系suo y
		fluxzM = np.diff(partialzM,axis=0)
		shape = (180,360)
		fluxzM = np.append(fluxzM,[np.ones(shape)],axis=0)
		fluxzM = np.divide(fluxzM, dz2)
		
		t1 = np.multiply(fluxzM,vol)
		
		valv = sum(t1[c])
		valv = valv*littled
		valv = valv/1000000
		
		mylist.append(valv)
	
	#print(mylist)
	print(dz1)
	plt.title("vertical mixing process with D value 0.00005")
	plt.plot(mylist)
	plt.show()







	# salinity = np.squeeze(sa[MON, :, :, :])
	# for i in range(101):
	# 	np.append(partialzM, np.diff(salinity[i,:,:],axis = 0)) #along the depth
	
	# print(partialzM.shape)
	# partialzM = np.array(partialzM)

	# partialzM = np.divide(partialzM, dz1)
	# partialzM = np.multiply(partialzM, 0.00005)

		


		
		