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
	i = 5
	m = maskMatrix(np.squeeze(sa[i, :, :, :]), RANGEA, RANGEB)
	b = m & ((gridx<280) & (gridx>200))
	c = b & (gridy<(-5))
	a = vol[c]
	plt.subplot(3,4,i+1)
	plt.imshow(c[0], extent=[xt.min(), xt.max(), yt.min(), yt.max()], interpolation='nearest', origin='lower')
	v5.append(sum(a))	
	v5.insert(0,v5[11])
	v5 = np.array(v5)
	d5 = np.diff(v5)
	svconvert = time*1000000
	d5 = [i/svconvert for i in d5]
	plt.figure(2)
	plt.plot(d5)




	i = 6
	m = maskMatrix(np.squeeze(sa[i, :, :, :]), RANGEA, RANGEB)
	b = m & ((gridx<280) & (gridx>200))
	c = b & (gridy<(-5))
	a = vol[c]
	plt.subplot(3,4,i+1)
	plt.imshow(c[0], extent=[xt.min(), xt.max(), yt.min(), yt.max()], interpolation='nearest', origin='lower')
	v5.append(sum(a))	
	v5.insert(0,v5[11])
	v5 = np.array(v5)
	d5 = np.diff(v5)
	svconvert = time*1000000
	d5 = [i/svconvert for i in d5]
	plt.figure(1)
	plt.plot(d5)
	plt.show()
