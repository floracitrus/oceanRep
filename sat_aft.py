import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
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

	gridx, gridy = np.meshgrid(xt,yt)
	RANA = 35.9
	RANB = 36.1
	MON = 5
	saJanSurf = np.squeeze(sa[MON, 0, :, :])
	circle = np.array(saJanSurf)
	circle = maskMatrix(saJanSurf, RANA, RANB)
	circle = np.logical_and(circle , np.logical_and(gridx<280, gridx>200))
	circle = np.logical_and(circle, gridy<0)


	newM = np.array(saJanSurf)

	# for i in range(180):
	# 	for j in range(360):
	# 		if(circle[i][j]==True):
	# 			newM[i][j] = saJanSurf[i][j]
	# 		else:
	# 			newM[i][j] = 36.1

	for i in range(180):
		for j in range(360):
			if(saJanSurf[i][j]>RANB):
				newM[i][j] = RANB
			elif(saJanSurf[i][j]<RANA):
				newM[i][j] = RANA
			else:
				newM[i][j] = saJanSurf[i][j]

	plt.figure(2)
	plt.title("the salinity world map of 35.9 to 36.1")
	plt.xlabel("longitude")
	plt.ylabel("latitude")
	plt.imshow(newM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                 interpolation='nearest', origin='lower',cmap ="seismic", vmin = RANA, vmax = RANB)
	
	plt.colorbar()
	#newM = np.array(saJanSurf) #DEBUG USE
	newxM = np.c_[newM, np.transpose(newM)[0]]  ##add an extra column	
	partialxM = []
	difx = dx[0,:,:]
	difx = np.roll(difx, 1, axis = 1)
	for i in range(180):
		partialxM.append(np.diff(newxM[i]))		
	partialxM = np.multiply(partialxM, 1000) #times K
	partialxM = np.divide(partialxM, difx)
	


	partialxM = np.c_[partialxM, np.transpose(partialxM)[0]]
	fluxxM = []
	for i in range(180):
		fluxxM.append(np.diff(partialxM[i]))	
	dif3x = dx[0,:,:]
	dif3x = np.roll(dif3x, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
	#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1 #WRONG

	difx = np.add(difx, dif3x) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
	difx = np.multiply(difx, 0.5)#1/2(x3-x1)
	difx = np.array(difx)
	#print(difx.shape())
	fluxxM = np.divide(fluxxM, difx)

	plt.subplot(2,1,1)
	plt.title("salt flux of salinity in x-dir 36(35.9->36.1)")
	plt.xlabel("longitude")
	plt.ylabel("latitude")
	plt.imshow(fluxxM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                 interpolation='nearest', origin='lower',cmap = "seismic")
	
	plt.colorbar()
	print(np.sum(fluxxM))
	sumPos = 0
	sumNeg = 0
	for i in range(180):
		for j in range(360):
			if(np.isnan(fluxxM[i][j])):
				sumPos = sumPos
				sumNeg = sumNeg
			elif(fluxxM[i][j]>0 and 200<j<270):
				sumPos += fluxxM[i][j]
				print("x positive")
				print(sumPos)
			elif(fluxxM[i][j]<0 and 200<j<270):
				sumNeg += fluxxM[i][j]
				print("x negative")
				print(sumNeg)
	# if(sumPos>(-sumNeg)):
	# 	print("true")
	# if(sumPos<(-sumNeg)): 
	# 	print("false")
	# else: 
	# 	print("equal")



	newyM = np.append(newM, [newM[0]],axis = 0)
	dify = dy[0,:,:]
	partialyM = []
	for i in range(360):
		partialyM.append(np.diff(np.transpose(newyM)[i]))
	partialyM = np.array(partialyM)
	partialyM = np.multiply(partialyM, 1000) #times K
	partialyM = np.divide(partialyM, np.transpose(dify))
	

	partialyM = np.c_[partialyM, np.transpose(partialyM)[0]]
	fluxyM = []
	for i in range(360):
		fluxyM.append(np.diff(partialyM[i]))	
	dif3y = dy[0,:,:]
	dif3y = np.roll(dif3y, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
	#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1 #WRONG

	dify = np.add(dify, dif3y) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
	dify = np.multiply(dify, 0.5)#1/2(x3-x1)
	dify = np.array(dify)
	#print(difx.shape())
	fluxyM = np.divide(fluxyM, np.transpose(dify))

	plt.subplot(2,1,2)
	plt.title("salt flux of salinity in y-dir 36(35.9->36.1)")
	plt.xlabel("longitude")
	plt.ylabel("latitude")
	plt.imshow(np.transpose(fluxyM), extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                 interpolation='nearest', origin='lower',cmap = "seismic")
	
	plt.colorbar()



	for i in range(360):
		for j in range(180):
			if(np.isnan(fluxyM[i][j])):
				sumPos = sumPos
				sumNeg = sumNeg
			elif(fluxyM[i][j]>0 and 210<i<270):
				sumPos += fluxyM[i][j]
				print("y positive")
				print(sumPos)
			elif(fluxyM[i][j]<0 and 210<i<270):
				sumNeg += fluxyM[i][j]
				print("y negative")
				print(sumNeg)





	plt.show()






	for i in range(180):
		for j in range(360):
			if(circle[i][j]==True):
				newM[i][j] = saJanSurf[i][j]
			else:
				newM[i][j] = 35.9

	plt.figure(2)
	plt.title("the salinity larger than 35.9")
	plt.imshow(newM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                 interpolation='nearest', origin='lower',vmin = 35.9, vmax = 37)
	
	#newM = np.array(saJanSurf) #DEBUG USE
	newM = np.c_[newM, np.transpose(newM)[0]]  ##add an extra column	
	partialxM = []
	difx = dx[0,:,:]
	difx = np.roll(difx, 1, axis = 1)
	for i in range(180):
		partialxM.append(np.diff(newM[i]))		
	partialxM = np.multiply(partialxM, 1000) #times K
	partialxM = np.divide(partialxM, difx)
	partialxM = np.c_[partialxM, np.transpose(partialxM)[0]]


	fluxxM = []
	for i in range(180):
		fluxxM.append(np.diff(partialxM[i]))	
	dif3x = dx[0,:,:]
	dif3x = np.roll(dif3x, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
	#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1

	difx = np.add(difx, dif3x) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
	difx = np.multiply(difx, 0.5)#1/2(x3-x1)
	difx = np.array(difx)
	#print(difx.shape())
	fluxxM = np.divide(fluxxM, difx)

	plt.figure(1)
	plt.title("flux_xdir_M")
	plt.imshow(fluxxM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                 interpolation='nearest', origin='lower',cmap = "seismic")
	
	plt.colorbar()
	print("dx is ")
	print(dx[0,:,:])
	print(difx)


	plt.show()





