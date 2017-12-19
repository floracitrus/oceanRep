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
	RANA = 35.95  #intrested range
	RANB = 36.05
	MON = 4 #month
	little_d = 10 #1/0.2
	totx = 0
	toty = 0
	for k in range(0,60):

		saJanSurf = np.squeeze(sa[MON, k, :, :])
		circle = np.array(saJanSurf)
		circle = maskMatrix(saJanSurf, RANA, RANB)
		circle = np.logical_and(circle , np.logical_and(gridx<280, gridx>200))
		circle = np.logical_and(circle, gridy<0)


		newM = np.array(saJanSurf)
		#not using 
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
		#to compute sum to comment
		# plt.figure(2)
		# plt.title("the salinity world map of 36.2 to 36.4")
		# plt.xlabel("longitude")
		# plt.ylabel("latitude")
		# plt.imshow(newM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
	 #                 interpolation='nearest', origin='lower',cmap ="seismic", vmin = 36.2, vmax = 36.4)
		
		# plt.colorbar()
		
		newxM = np.c_[newM, np.transpose(newM)[0]]  ##add an extra column	
		partialxM = []
		difx = dx[k,:,:]
		difx = np.roll(difx, 1, axis = 1)
		for i in range(180):
			partialxM.append(np.diff(newxM[i]))		
		partialxM = np.multiply(partialxM, 1000) #times K
		partialxM = np.divide(partialxM, difx)
		


		partialxM = np.c_[partialxM, np.transpose(partialxM)[0]]
		fluxxM = []
		for i in range(180):
			fluxxM.append(np.diff(partialxM[i]))	
		dif3x = dx[k,:,:]
		dif3x = np.roll(dif3x, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
		#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1 #WRONG

		difx = np.add(difx, dif3x) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
		difx = np.multiply(difx, 0.5)#1/2(x3-x1)
		difx = np.array(difx)
		#print(difx.shape())
		fluxxM = np.divide(fluxxM, difx)
		#comment for calculate the sum
		# plt.subplot(2,1,1)
		# plt.title("salt flux of salinity in x-dir 36.3(36.4->36.2)")
		# plt.xlabel("longitude")
		# plt.ylabel("latitude")
		# plt.imshow(fluxxM, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
	 #                 interpolation='nearest', origin='lower',cmap = "seismic")
		
		# plt.colorbar()
		# print(np.sum(fluxxM))
		sumxPos = 0
		sumxNeg = 0
		for i in range(180):
			for j in range(360):
				if(np.isnan(fluxxM[i][j])):
					sumxPos = sumxPos
					sumxNeg = sumxNeg
				elif(fluxxM[i][j]>0 and 210<j<270):
					sumxPos += fluxxM[i][j]
					#print("x positive")
					#print(sumPos)
				elif(fluxxM[i][j]<0 and 210<j<270):
					sumxNeg += fluxxM[i][j]
					#print("x negative")
					#print(sumNeg)
		totx += (sumxNeg*little_d+sumxPos*little_d)
		# print("x")
		# print(sumNeg*5+sumPos*5)

		newyM = np.append(newM, [newM[0]],axis = 0)
		dify = dy[k,:,:]
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
		dif3y = dy[k,:,:]
		dif3y = np.roll(dif3y, 2, axis = 1)#x3,x4,...x359,x0,x1,x2
		#difx = np.subtract(dif3x, dx[0,:,:])#x3-x1 #WRONG

		dify = np.add(dify, dif3y) #1/2(x3-x1= x1+x2+x3-x1) = 1/2(x2+x3)
		dify = np.multiply(dify, 0.5)#1/2(x3-x1)
		dify = np.array(dify)
		#print(difx.shape())
		fluxyM = np.divide(fluxyM, np.transpose(dify))


		#comment for calculate the sum
		# plt.subplot(2,1,2)
		# plt.title("salt flux of salinity in y-dir 36.3(36.4->36.2)")
		# plt.xlabel("longitude")
		# plt.ylabel("latitude")
		# plt.imshow(np.transpose(fluxyM), extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
	 #                 interpolation='nearest', origin='lower',cmap = "seismic")
		
		# plt.colorbar()

		sumyPos = 0
		sumyNeg = 0
		for i in range(360):
			for j in range(180):
				if(np.isnan(fluxyM[i][j])):
					sumyPos = sumyPos
					sumyNeg = sumyNeg
				elif(fluxyM[i][j]>0 and 210<i<270):
					sumyPos += fluxyM[i][j]
					#print("y positive")
					#print(sumPos)
				elif(fluxyM[i][j]<0 and 210<i<270):
					sumyNeg += fluxyM[i][j]
					#print("y negative")
					#print(sumNeg)

		toty += (sumyNeg*little_d+sumyPos*little_d)
	
	print("x")
	print(totx)
	print("y")
	print(toty)
	#Jan 36 
	#x -8.56380491554e-07
	#y -5.54179887545e-07
	#z -3.13289551605e-06 #-3.13289551605e-06

	#Feb 36
	#x -5.85920495602e-07
	#y -1.69344682875e-06
	#z -6.87544574666e-05

	#March 36
	#z -1.73715758006e-05
	#x -1.51919561696e-06
	#y -5.16519592317e-07
	#May 36
	#z -3.60239819246e-05

	#Jun 36
	#z -4.48286999009e-05 #-4.98222107795e-05
	#x -6.54663134095e-08
	#y -1.06391403161e-06
	



	#Dec 36
	#with 0.05
	#x 1.58546154258e-07
	#y -1.25567003788e-06
	#z -5.21377100824e-05
	#with 0.1
	#x 2.26488684856e-07
	#y -1.28290195804e-06
	#z -4.03433845903e-05




	#plt.show()





