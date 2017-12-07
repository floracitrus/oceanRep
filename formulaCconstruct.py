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
	
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	zt = np.squeeze(zzt)

	sa  = np.squeeze(ssa)
	axy = np.squeeze(aaxy)
	ayz = np.squeeze(aayz)
	vol = np.squeeze(vol)

############line 	
	plt.figure(1)
	gridx, gridy = np.meshgrid(xt,yt)
	volrawList = []#the monthly volList
	#print(vol)

	for i in range(12):
		v = 0 
		for j in range(101):
			m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.1)
			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
			vTemp = np.squeeze(vol[j,:,:])
			v += sum(vTemp[m])
		volrawList.append(v)


	# for i in range(12):
	# 	vvol = 0
	# 	for j in range(101):#range zt 0-100
	# 		m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
	# 		m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
	# 		axy2d = np.squeeze(axy[j,:,:])#each thick layer in z direction
	# 		if j<20:
	# 			a = axy2d[m]*5
	# 		elif j>=20 and j<36:
	# 			a = axy2d[m]*25
	# 		elif j>=36:
	# 			a = axy2d[m]*50
	# 		vvol += sum(a)

	# 	volrawList.append(vvol)

	#volList = volrawList

	#####################normalize############################################
	# aver = np.average(volrawList)
	# var = np.var(volrawList)
	# volList = [(i-aver)/np.sqrt(var) for i in volrawList]

	plt.title("volume of north pacific ocean circle region monthly graph")
	plt.ylabel('volume of the circle')
	plt.xlabel('Month')
	plt.plot(volrawList)
	
#########line diff

	plt.figure(3)
	plt.title("dv/dt of certain region monthly graph")
	JanVol = volrawList[0]
	volrawList.append(JanVol) #made a 
	diffVolList = np.diff(volrawList)
	time = 365*24*3600/12
	svconvert = time*1000000
	diffVolList = [i/svconvert for i in diffVolList]
	plt.ylabel('dv/dt svandrup')
	plt.xlabel('Month')
	plt.plot(diffVolList)


	plt.figure(2)
	m = maskMatrix(np.squeeze(sa[i, 0, :, :]), 36.0, 36.1)
	mask = m & ((gridx<280) & (gridx>200))
	circleOnly = mask & (gridy<0)
	plt.imshow(circleOnly, extent=[xt.min(), xt.max(), yt.min(), yt.max()], 
                interpolation='nearest', origin='lower')
	plt.plot()


##########bar
	# plt.figure(2)
	# gridx, gridy = np.meshgrid(xt,yt)
	# volList = []#the monthly volList
	# for i in range(0, 12):
	# 	for j in range(101):#range zt 0-100
	# 		m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
	# 		m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
	# 		vvol = np.squeeze(vol[j,:,:])#each layer in z direction
	# 		vvol
	# 	volList.append(vol)
	# x = range(0,12)
	# rects1 = plt.bar(x,volList)
	# plt.title("volume of certain region monthly graph")
	# plt.ylabel('volume of the circle')
	# plt.xlabel('Month')
	

###############
	#So from article we want to calculate the tendency of tracer C, 
	#in here we first construct the first term of that formula the d_c horizontal
	#which is the one operates in the mixed layer on horizontal tracer gradients.
	#tracer ﬂux given by K∇NC  





	plt.show()

