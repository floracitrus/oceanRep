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
	
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	zt = np.squeeze(zzt)

	sa  = np.squeeze(ssa)
	axy = np.squeeze(aaxy)
	ayz = np.squeeze(aayz)

############line 	
	plt.figure(1)
	gridx, gridy = np.meshgrid(xt,yt)
	volrawList = []#the monthly volList
	for i in range(12):
		vol = 0
		for j in range(101):#range zt 0-100
			m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
			axy2d = np.squeeze(axy[j,:,:])#each layer in z direction
			a = axy2d[m]
			vol += sum(a)

		volrawList.append(vol)

	#volList = volrawList
	aver = np.average(volrawList)
	var = np.var(volrawList)
	volList = [(i-aver)/np.sqrt(var) for i in volrawList]

	plt.title("volume of north pacific ocean circle region monthly graph")
	plt.ylabel('volume of the circle')
	plt.xlabel('Month')
	plt.plot(volList)
	
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


##########bar
	plt.figure(2)
	gridx, gridy = np.meshgrid(xt,yt)
	volList = []#the monthly volList
	for i in range(0, 12):
		vol = 0
		for j in range(101):#range zt 0-100
			m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
			axy2d = np.squeeze(axy[j,:,:])#each layer in z direction
			a = axy2d[m]
			vol += sum(a)
		volList.append(vol)
	x = range(0,12)
	rects1 = plt.bar(x,volList)
	plt.title("volume of certain region monthly graph")
	plt.ylabel('volume of the circle')
	plt.xlabel('Month')
	

##########bow shape
	# plt.figure(4)
	# ax = fig.gca(projection='3d')


##########






	plt.show()

