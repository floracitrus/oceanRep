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
	#totz = 0
	time = 365*24*3600/12
	gridx, gridy = np.meshgrid(xt,yt)

	fluxzM = np.zeros((101,180,360))
	fluxxM = np.zeros((101,180,360))
	fluxyM = np.zeros((101,180,360))
	vlisth = []
	vlistv = []
	for MON in range(12):
		#vertical with fixed range of longtitude which is the part that circle allocated in 
		#####################vertical
		for k in range(360):
		
			saJanSurf = np.squeeze(sa[MON, :, :, k])
			newM = np.array(saJanSurf)
			newM[ newM > RANB ] = RANB
			newM[ newM < RANA ] = RANA


			#add the last col to first for calculate the first one
			newzM = np.c_[np.transpose(newM)[11], newM]
			partialzM = []
			
			#(x1+x2)/2
			difz = dz[:,:,k]
			dif1z = np.roll(difz, 1, axis = 1)
			difz = np.add(difz, dif1z)
			difz = np.multiply(difz, 0.5)

			
			for i in range(101):
				partialzM.append(np.diff(newzM[i]))		
			
			#times D 5e-05
			partialzM = np.multiply(partialzM, 0.00005) 
			partialzM = np.divide(partialzM, difz)
			

			partialzM = np.c_[np.transpose(partialzM)[11], partialzM]
			fluxz2dM = []
			for i in range(101):
				fluxz2dM.append(np.diff(partialzM[i]))
			fluxz2dM = np.array(fluxz2dM)
			fluxzM[:,:,k] = fluxz2dM

			#maybe problem double check
			dif3z = dz
			dif2z = dz
			dif3z = np.roll(dif3z, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
			dif2z = np.add(dif2z, dif3z) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
			dif2z = np.multiply(dif2z, 0.5)#1/2(x3-x1)
			dif2z = np.array(dif2z)
		
		fluxzM = np.divide(fluxzM, dif2z)
		#print(fluxzM)
		#################horizontal
		for i in range(101):
		
			saJanSurf = np.squeeze(sa[MON, i, :, :])
			newM = np.array(saJanSurf)
			newM[ newM > RANB ] = RANB
			newM[ newM < RANA ] = RANA


			#add the last col to first for calculate the first one
			newxM = np.c_[np.transpose(newM)[11], newM]
			partialxM = []
			
			#(x1+x2)/2
			difx = dx[i,:,:]
			dif1x = np.roll(difx, 1, axis = 1)
			difx = np.add(difx, dif1x)
			difx = np.multiply(difx, 0.5)

			
			for j in range(180):
				partialxM.append(np.diff(newxM[j]))		
			partialxM = np.multiply(partialxM, 1000) #times K
			partialxM = np.divide(partialxM, difx)
			

			partialxM = np.c_[np.transpose(partialxM)[11], partialxM]
			fluxx2dM = []
			for j in range(180):
				fluxx2dM.append(np.diff(partialxM[j]))	
			fluxx2dM = np.array(fluxx2dM)
			dif3x = dx
			dif2x = dx
			dif3x = np.roll(dif3x, 2, axis = 1)
			dif2x = np.add(dif2x, dif3x)
			dif2x = np.multiply(dif2x, 0.5)
			dif2x = np.array(dif2x)

			fluxxM[i,:,:] = fluxx2dM

			
			newyM = np.append(newM, [newM[0]],axis = 0)
			dify = dy[i,:,:]
			partialyM = []
			for k in range(360):
				partialyM.append(np.diff(np.transpose(newyM)[k]))
			partialyM = np.array(partialyM)
			partialyM = np.multiply(partialyM, 1000) #times K
			partialyM = np.divide(partialyM, np.transpose(dify))
			

			partialyM = np.c_[np.transpose(partialyM)[11], partialyM]
			fluxy2dM = []
			for k in range(360):
				fluxy2dM.append(np.diff(partialyM[k]))	
			dif3y = dy
			dif2y = dy
			dif3y = np.roll(dif3y, 2, axis = 1)
			dif2y = np.add(dif2y, dif3y)
			dif2y = np.multiply(dif2y, 0.5)
			dif2y = np.array(dif2y)


			fluxyM[i,:,:] = np.transpose(fluxy2dM)
		
		fluxxM = np.divide(fluxxM,dif2x)
		fluxyM = np.divide(fluxyM,dif2y)
			
		#print(fluxxM)
		sdoth = np.add(fluxyM,fluxxM)
		sdotv = np.array(fluxzM)
		sdoth = np.array(sdoth)

		valv = 0
		valh = 0
		m = maskMatrix(np.squeeze(sa[MON, :, :, :]), 35.9, 36.1)
		m = m & ((gridx<280) & (gridx>200))
		#print(vol[m])

		for i in range(101):
			for j in range(180):
				for k in range(360):
					if not np.isnan(sdoth[i][j][k]) and (35.9<sa[MON,i,j,k]<36.1) and np.nonzero(sdoth[i][j][k]):
						valh += sdoth[i][j][k]*vol[i][j][k]
					if not np.isnan(sdotv[i][j][k]) and (35.9<sa[MON,i,j,k]<36.1) and np.nonzero(sdotv[i][j][k]):
						valv += sdotv[i][j][k]*vol[i][j][k]
		
		valh = valh*littled
		valh = valh/1000000
		
		vlisth.append(valh)
		valv = valv*littled
		valv = valv/1000000
		
		vlistv.append(valv)
	
	plt.figure()
	plt.plot(vlistv)
	plt.plot(vlisth)
	plt.legend(['vertical mixing sa dot', 'horizontal mixing sa dot'], loc='upper left')
	plt.xlabel('Month')
	plt.ylabel('changes of volume in svandrup by mixing')






	# v = np.multiply(sdot, vol)
	# m = maskMatrix(np.squeeze(sa[MON, :, :, :]), 35.9, 36.1)
	# m = m & ((gridx<280) & (gridx>200))
	# vt = sum(v[m])
	
	#print(vt)
	#vlist.append(vt)	
	# volList = [-652663.169149,-746266.288002,-711537.604518,-733834.16875,-915989.792616,-734469.03343,-764119.198171,-704553.574485,-794743.330259,-615978.965556,-805162.564102,-823308.161848]
	# plt.figure(1)
	# x = range(1,13)
	# rects1 = plt.bar(x,volList)
	# #plt.plot(vlist)

	plt.show()






