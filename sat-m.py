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
	aaxy = list(file['Axy']) #101x
	E_Core = list(file['E_Core'])
	P_Core = list(file['P_Core'])
	R_Core = list(file['R_Core'])
	
	sa  = np.squeeze(ssa)
	dz = np.squeeze(dz)
	dx = np.squeeze(dx)
	dy = np.squeeze(dy)
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	vol = np.squeeze(vol)

	axy = np.squeeze(aaxy)
	E_Core = np.squeeze(E_Core)
	P_Core = np.squeeze(P_Core)
	R_Core = np.squeeze(R_Core)
	
	RANA = 35.9
	RANB = 36.1
	littled = 5
	
	gridx, gridy = np.meshgrid(xt,yt)

	#dx
	dx1 = np.add(dx,np.roll(dx,1,axis = 2))
	dx1 = np.multiply(dx1,0.5)
	
	dx2 = np.add(dx, np.roll(dx, 2, axis = 2))
	dx2 = np.multiply(dx2,0.5)
	
	#dy
	dy1 = np.add(dy,np.roll(dy,1,axis = 2))
	dy1 = np.multiply(dy1,0.5)
	
	dy2 = np.add(dy, np.roll(dy, 2, axis = 2))
	dy2 = np.multiply(dy2,0.5)

	#dz
	dz1 = np.add(dz,np.roll(dz,1, axis = 0))
	dz1 = np.multiply(dz1,0.5)
	
	dz2 = np.add(dz, np.roll(dz, 2, axis = 0))
	dz2 = np.multiply(dz2,0.5)
	

	MON = 0
	mylist = []
	mylist1 = []

	asf = np.add(E_Core,P_Core)
	asf = np.add(asf, -R_Core)
	ss = np.squeeze(sa[:,0,:,:])
	fs = np.multiply(asf,ss)
	saxy = np.squeeze(axy[0,:,:])
	f = []
	time = 365*24*3600/12
	gridx, gridy = np.meshgrid(xt,yt)
	RANGEA = 35.98
	RANGEB = 38.5
	v5=[]

	for MON in range(12):

		#每一个mask只对应那个月里面所有圈圈里的方块的坐标和值
		mask = maskMatrix(np.squeeze(sa[MON,:,:,:]),RANA,RANB)
		mask = mask & ((gridx<280) & (gridx>185))
		b = mask & (gridy<(-5)) 
		c = b & (gridy>(-60))
		#c取到了这个圈圈馁的所有的点

		salinity = np.squeeze(sa[MON, :, :, :])
		
		partialxM = np.diff(salinity,axis=2)
		shape = (101,180,1)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		

		partialxM = np.append(partialxM,np.ones(shape),axis = 2)
		
		partialxM = np.divide(partialxM, dx1)
		partialxM = np.multiply(partialxM, 1000) #times K
		#因为知道最后两行没关系
		fluxxM = np.diff(partialxM,axis=2)
		
		fluxxM = np.append(fluxxM,np.ones(shape),axis=2)
		fluxxM = np.roll(fluxxM, 1, axis = 2)
		fluxxM = np.divide(fluxxM, dx2)
		
		t1 = np.multiply(fluxxM,vol)
		

		partialyM = np.diff(salinity,axis=1)
		shape = (101,1,360)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		partialyM = np.append(partialyM,np.ones(shape),axis=1)

		partialyM = np.divide(partialyM, dy1)
		partialyM = np.multiply(partialyM, 1000) #times K
		#因为知道最后两行没关系
		fluxyM = np.diff(partialyM,axis=1)
		
		fluxyM = np.append(fluxyM,np.ones(shape),axis=1)
		fluxyM = np.roll(fluxyM, 1, axis = 2)
		fluxyM = np.divide(fluxyM, dy2)
		
		t2 = np.multiply(fluxyM,vol)



		valh = sum(t1[c]+t2[c])
		valh = valh*littled
		valh = valh/1000000
		
		mylist.append(valh)



		partialzM = np.diff(salinity,axis=0)
		shape = (180,360)
		#error estimate happens here, I put the 100th layer last full of ones
		#to match the dimension 101*180*360
		partialzM = np.append(partialzM,[np.ones(shape)],axis=0)
		partialzM = np.divide(partialzM, dz1)
		partialzM = np.multiply(partialzM, 0.00005) 
		
		fluxzM = np.diff(partialzM,axis=0)
		fluxzM = np.append(fluxzM,[np.ones(shape)],axis=0)
		fluxzM = np.roll(fluxzM, 1, axis = 2)
		fluxzM = np.divide(fluxzM, dz2)
		
		t3 = np.multiply(fluxzM,vol)
		
		valv = sum(t3[c])
		valv = valv*littled
		valv = valv/1000000
		
		mylist1.append(valv)


		term = np.multiply(fs[MON, :, :],saxy)
		mask = maskMatrix(np.squeeze(sa[MON,0,:,:]),RANA,RANB)
		mask = mask & ((gridx<280) & (gridx>185))
		b = mask & (gridy<(-5)) 
		c =	b & (gridy>(-60))
	
		su = sum(term[c])
		su = su*littled
		su = su/1000000
		f.append(su)

		m = maskMatrix(np.squeeze(sa[MON, :, :, :]), RANGEA, RANGEB)
		m = m & ((gridx<280) & (gridx>185))
		b = m & (gridy<(-5)) 
		c =	b & (gridy>(-60))
		a = vol[c]
		v5.append(sum(a))


	#v5.insert(0,v5[11])
	v5 = np.array(v5)
	v6 = np.roll(v5,1)
	d5 = np.subtract(v6,v5)
	svconvert = time*1000000
	d5 = [i/svconvert for i in d5]

	estimate5 = np.add(mylist,mylist1)
	estimate5 = np.add(estimate5,f)

	print(mylist1)
	print(mylist)
	print(f)

	plt.title("horizontal and vertical mixing process with K,D and air-sea flux")
	plt.plot(mylist1)
	plt.plot(mylist)
	plt.plot(f)
	plt.plot(d5)
	plt.plot(estimate5)
	plt.legend(['vertical mixing sa dot', 'horizontal mixing sa dot','air-sea flux','the salinity volume change in ball','sum of sa dot and air-sea flux'])
	plt.xlabel('Month')
	plt.ylabel('changes of volume in svandrup by mixing')
	





	plt.show()


		
		