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
	dx = list(file['dx'])
	dy = list(file['dy'])
	vol = list(file['vol'])
	sa  = np.squeeze(ssa)
	dz = np.squeeze(dz)
	dx = np.squeeze(dx)
	dy = np.squeeze(dy)
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	vol = np.squeeze(vol)
	
	RANA = 35.9
	RANB = 36.1
	littled = 5
	
	gridx, gridy = np.meshgrid(xt,yt)

	#dz
	dx1 = np.add(dx,np.roll(dx,1,axis = 2))
	dx1 = np.multiply(dx1,0.5)
	
	dx2 = np.add(dx, np.roll(dx, 2, axis = 2))
	dx2 = np.multiply(dx2,0.5)
	print(dx1.shape)

	MON = 0
	mylist = []
	for MON in range(12):

		#每一个mask只对应那个月里面所有圈圈里的方块的坐标和值
		mask = maskMatrix(np.squeeze(sa[MON,:,:,:]),RANA,RANB)
		mask = mask & ((gridx<280) & (gridx>200))
		c = mask & (gridy<(-5))
		#c取到了这个圈圈馁的所有的点

		salinity = np.squeeze(sa[MON, :, :, :])
		
		partialxM = np.diff(salinity,axis=2)
		shape = (101,180)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		print(partialxM.shape)
		partialxM = np.append(partialxM,[np.ones(shape)],axis = 2)
		partialxM = np.divide(partialxM, dx1)
		partialxM = np.multiply(partialxM, 1000) #times K
		#因为知道最后两行没关系
		fluxxM = np.diff(partialzM,axis=2)
		print(fluxxM.shape)
		fluxxM = np.append(fluxxM,[np.ones(shape)],axis=2)
		fluxxM = np.divide(fluxxM, dx2)
		
		t1 = np.multiply(fluxxM,vol)
		

		partialyM = np.diff(salinity,axis=1)
		shape = (101,360)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		partialyM = np.append(partialyM,[np.ones(shape)],axis=1)
		partialyM = np.divide(partialyM, dy1)
		partialyM = np.multiply(partialyM, 1000) #times K
		#因为知道最后两行没关系
		fluxyM = np.diff(partialyM,axis=1)
		
		fluxyM = np.append(fluxyM,[np.ones(shape)],axis=1)
		fluxyM = np.divide(fluxyM, dy2)
		
		t2 = np.multiply(fluxyM,vol)



		valh = sum(t1[c]+t2[c])
		valh = valh*littled
		valh = valh/1000000
		
		mylist.append(valh)
	
	#print(mylist)
	print(dx1)
	plt.title("horizontal mixing process with K value 1000")
	plt.plot(mylist)
	plt.show()


		
		