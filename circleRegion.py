import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math
#function1
# def normalize(lst):
#      s = sum(lst)
#      return map(lambda x: float(x/s), lst)

def maskMatrix(matrix, rangeA, rangeB):
	np.errstate(invalid='ignore')
	m = (matrix>=rangeA) & (matrix<rangeB) 
	#selected = matrix[m] #a list of selected points
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

	time = 365*24*3600/12
	gridx, gridy = np.meshgrid(xt,yt)
	RANGEA = 36
	RANGEB = 39


	plt.figure()
	v5=[]
	for i in range(12):
		m = maskMatrix(np.squeeze(sa[i, :, :, :]), RANGEA, RANGEB)
		m = m & ((gridx<280) & (gridx>200))
		m = m & gridy<(-5)
		a = vol[m]
		plt.subplot(3,4,i+1)
		plt.imshow(m[0], extent=[xt.min(), xt.max(), yt.min(), yt.max()], interpolation='nearest', origin='lower')
		v5.append(sum(a))	
	v5.append(v5[0])
	v5 = np.array(v5)
	d5 = np.diff(v5)
	svconvert = time*1000000
	d5 = [i/svconvert for i in d5]
	plt.plot(d5)
	plt.show()

##################line volume change dv/dt
# 	plt.figure(4)
# 	vlist = []
# 	for i in range(12):
# 		v = 0
# 		for j in range(101):#range zt 0-100
# 			m = maskMatrix(np.squeeze(sa[i, j, :, :]), RANGEA, RANGEB)
# 			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 			vxy = np.squeeze(vol[j,:,:])#each layer in z direction
# 			a = vxy[m]
# 			v += sum(a)
# 		vlist.append(v)
# 	vlist.insert(0,vlist[11]) #the 13th element
# 	vlist = np.array(vlist)
# 	dlist = np.diff(vlist)
# 	dlist = [i/time for i in dlist]
# 	dlist = [i/1000000 for i in dlist]
# 	plt.xlabel("month")
# 	plt.ylabel("the change of volume the region (svandrup)")
# 	plt.plot(dlist)



# ############line 	
# 	plt.figure(1)
	
# 	volrawList = []#the monthly volList
# 	for i in range(12):
# 		vol = 0
# 		for j in range(101):#range zt 0-100
# 			m = maskMatrix(np.squeeze(sa[i, j, :, :]), RANGEA, RANGEB)
# 			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 			axy2d = np.squeeze(axy[j,:,:])#each layer in z direction
# 			a = axy2d[m]
# 			vol += sum(a)

# 		volrawList.append(vol)

# 	#volList = volrawList
# 	aver = np.average(volrawList)
# 	var = np.var(volrawList)
# 	volList = [(i-aver)/np.sqrt(var) for i in volrawList]

# 	plt.title("volume of south pacific ocean circle region monthly graph")
# 	plt.ylabel('volume of the circle')
# 	plt.xlabel('Month')
# 	plt.plot(volList)
	
# #########line diff
# 	plt.figure(3)
# 	plt.title("dv/dt of certain region monthly graph")
# 	JanVol = volrawList[0]
# 	volrawList.append(JanVol) #made a 
# 	diffVolList = np.diff(volrawList)
# 	#time = 365*24*3600/12
# 	svconvert = time*1000000
# 	diffVolList = [i/svconvert for i in diffVolList]

# 	plt.ylabel('dv/dt svandrup')
# 	plt.xlabel('Month')
# 	plt.plot(diffVolList)


# ##########bar
# 	plt.figure(2)
# 	gridx, gridy = np.meshgrid(xt,yt)
# 	volList = []#the monthly volList
# 	for i in range(0, 12):
# 		vol = 0
# 		for j in range(101):#range zt 0-100
# 			m = maskMatrix(np.squeeze(sa[i, j, :, :]), RANGEA, RANGEB)
# 			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 			axy2d = np.squeeze(axy[j,:,:])#each layer in z direction
# 			a = axy2d[m]
# 			vol += sum(a)
# 		volList.append(vol)
# 	x = range(0,12)
# 	rects1 = plt.bar(x,volList)
# 	plt.title("volume of certain region monthly graph")
# 	plt.ylabel('volume of the circle')
# 	plt.xlabel('Month')
	

# ##########bow shape
# 	# plt.figure(4)
# 	# ax = fig.gca(projection='3d')


# ##########

# ##########bar
# 	# plt.figure(2)
# 	# gridx, gridy = np.meshgrid(xt,yt)
# 	# volList = []#the monthly volList
# 	# for i in range(0, 12):
# 	# 	for j in range(101):#range zt 0-100
# 	# 		m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
# 	# 		m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 	# 		vvol = np.squeeze(vol[j,:,:])#each layer in z direction
# 	# 		vvol
# 	# 	volList.append(vol)
# 	# x = range(0,12)
# 	# rects1 = plt.bar(x,volList)
# 	# plt.title("volume of certain region monthly graph")
# 	# plt.ylabel('volume of the circle')
# 	# plt.xlabel('Month')
	


# 	# for i in range(12):
# 	# 	vvol = 0
# 	# 	for j in range(101):#range zt 0-100
# 	# 		m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
# 	# 		m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
# 	# 		axy2d = np.squeeze(axy[j,:,:])#each thick layer in z direction
# 	# 		if j<20:
# 	# 			a = axy2d[m]*5
# 	# 		elif j>=20 and j<36:
# 	# 			a = axy2d[m]*25
# 	# 		elif j>=36:
# 	# 			a = axy2d[m]*50
# 	# 		vvol += sum(a)

# 	# 	volrawList.append(vvol)

# 	#volList = volrawList

# 	#####################normalize############################################
# 	# aver = np.average(volrawList)
# 	# var = np.var(volrawList)
# 	# volList = [(i-aver)/np.sqrt(var) for i in volrawList]



# 	plt.show()

