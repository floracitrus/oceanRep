import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
#function1
# def normalize(lst):
#      s = sum(lst)
#      return map(lambda x: float(x/s), lst)

#this saltflux function is when K is a constant
# def simplifedSaltFlux(matrix):
# 	k = 1000 #m^2/s
# 	for i in matrix[0].np.diff(matrix[i])

def filter_sa(low, up):
	def helper(v):
		return v if(v>=low and v<=up) else 0
	return helper




def maskMatrix(matrix, rangeA, rangeB):
	np.errstate(invalid='ignore')
	m = (matrix>=rangeA) & (matrix<rangeB) 
	return m


RANA = 36.0
RANB = 37.0#not the hollo-circle, becomes the ball 



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

############line 	
# 	plt.figure(1)
	gridx, gridy = np.meshgrid(xt,yt)
# 	volrawList = []#the monthly volList
# 	#print(vol)

# 	for i in range(12):
# 		v = 0 
# 		for j in range(101):
# 			m = maskMatrix(np.squeeze(sa[i, j, :, :]), RANA, RANB)
# 			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 			vTemp = np.squeeze(vol[j,:,:])
# 			v += sum(vTemp[m])
# 		volrawList.append(v)


# 	plt.title("volume of north pacific ocean circle region monthly graph")
# 	plt.ylabel('volume of the circle')
# 	plt.xlabel('Month')
# 	plt.plot(volrawList)
	
# #########line diff

# 	plt.figure(2)
# 	plt.title("dv/dt of certain region monthly graph")
# 	JanVol = volrawList[0]
# 	volrawList.append(JanVol) #made a 
# 	diffVolList = np.diff(volrawList)
# 	time = 365*24*3600/12
# 	svconvert = time*1000000
# 	diffVolList = [i/svconvert for i in diffVolList]
# 	plt.ylabel('dv/dt svandrup')
# 	plt.xlabel('Month')
# 	plt.plot(diffVolList)

###############
	#salinity change 
	#january surface
	#plt.figure(3)
	saJanSurf = np.squeeze(sa[0, 0, :, :])
	circle = np.array(saJanSurf)
	circle = maskMatrix(saJanSurf, RANA, RANB)
	circle = np.logical_and(circle , np.logical_and(gridx<280, gridx>200))
	circle = np.logical_and(circle, gridy<0)
###########################################
	# plt.imshow(circle, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
 #                interpolation='nearest', origin='lower')
	
	# plt.plot()
	# plt.show()



############################################
	#newM = [list(map(filter_sa(RANA,RANB), x)) for x in saJanSurf]
	#newM = np.array(newM)
	newM = np.array(saJanSurf)

	for i in range(180):
		for j in range(360):
			if(circle[i][j]==True):
				newM[i][j] = saJanSurf[i][j]
			else:
				newM[i][j] = 0

	#print(newM)
	
#############################################
	#want to eliminate the all zero row and column but not yet
	
	partialxM = []
	for i in range(180):
		partialxM.append(np.diff(newM[i]))
	partialxM = np.array(partialxM)
	##########method 1
	#partialM = np.c_[ partialxM, np.zeros(180) ]

	#partialxM = np.divide(partialxM, dx[0,:,:])
	##########method 2
	b = np.zeros((180,360))
	b[:,:-1] = partialxM
	arrayxM = np.divide(b, dx[0,:,:])

	partialyM = []
	for i in range(360):
		partialyM.append(np.diff(np.transpose(newM)[i]))


	partialyM = np.array(partialyM)
	partialyM = np.c_[ partialyM, np.zeros(360) ]  
	partialyM = np.divide(partialyM, np.transpose(dy[0,:,:]))



	print("partial x Matrix with all non zero values")
	row,col = np.nonzero(arrayxM)
	print(arrayxM[row, col])
	print("partial y Matrix")
	print(partialyM)

	# print("xtttttttttttt")
	# print(dx[0,:,:])

	# print("ytttttttttttt")
	# print(dy[0,:,:])

	





	

