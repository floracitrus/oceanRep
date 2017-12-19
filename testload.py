#import  scipy.io as spio
import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
#as from v7.3 matlab using h5py


# def effectionPlot(sa_bf,intrest_min, intrest_max):
# 	#basic iteration
# 	newsa =deepcopy(sa_bf)
# 	for i in range(len(sa_bf)):
# 		for j in range(len(sa_bf[i])):
# 			if np.isnan(sa_bf[i][j]):
# 				newsa[i][j] = 0

# 			elif sa_bf[i][j]>intrest_min and sa_bf[i][j]<intrest_max:
# 				newsa[i][j] = 1
# 				lst.append()
# 			else:
# 				newsa[i][j] = 0
	
# 	return newsa




with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	#print(list(file.keys()))
	xxt = list(file['xt']) #360
	yyt = list(file['yt']) #180
	ssa = list(file['SA']) 
	zzt = list(file['zt'])

	xt = np.squeeze(xxt) #0~359.5
	yt = np.squeeze(yyt) #-89.5~89.5
	zt = np.squeeze(zzt)

	sa = np.squeeze(ssa)
	sa3d = np.squeeze(sa[0, :, :, :]) #fixed the January
	sa2dxy = np.squeeze(sa3d[0, :, :]) #fixed the layer z to 1
	sa2dyz = np.squeeze(sa3d[:, :, 215])#fixed layer x to 216

	lst = map(max, sa2dxy)
	z_max = max(lst)
	#
	#lst = map(min, sa2dxy)
	#z_min = min(lst)

	#print(z_max) #nan
	#print(z_min) #nan
	print(sa.shape)
	print(sa3d.shape)
	print(sa2dxy.shape)
	
	plt.figure()#figure1
	# plt.subplot(2, 2, 1)
	# cs = plt.contourf(xt, yt, sa2dxy)
	# #plt.clabel(cs, inline=1, fontsize=10) #with contour in line
	# plt.title('The coutour plot of dx dy and salinity')
	# plt.colorbar(cs, shrink = 0.8, extend = 'both') #using the default color schema


	# plt.subplot(2, 2, 2)
	# plt.pcolor(xt, yt, sa2dxy, cmap='RdBu',vmin=30, vmax=33)	
	# plt.title('dx dy on surfacez')
	# plt.axis([xt.min(), xt.max(), yt.min(), yt.max()])
	# plt.colorbar()


	# plt.subplot(2, 2, 3)
	# plt.imshow(sa2dxy, cmap='BrBG', extent=[xt.min(), xt.max(), yt.min(), yt.max()],
 #           interpolation='nearest', origin='lower')
	# plt.title('image pcolor')
	# plt.colorbar()

	# #got new min and max in yz plane
	# lst = map(max, sa2dyz)
	# z_max = max(lst)
	# lst = map(min, sa2dyz)
	# z_min = min(lst)

	plt.subplot(2, 2, 4)
	plt.pcolor(yt, zt, sa2dyz,cmap='Spectral',vmin=34, vmax=36)	
	plt.title('y-z in x-216 level')
	#plt.title('The pcolor plot of dy dz and salinity')
	plt.axis([yt.min(), yt.max(), zt.min(), zt.max()])
	plt.colorbar()
	plt.gca().invert_yaxis()

	plt.subplot(2, 2, 1)
	sa_bf = np.array(sa2dyz) #salinity before arraylize


	intrest_min = 34
	intrest_max = 36.3
	#call function
	#print(sa_bf.shape)
	newsa = effectionPlot(sa_bf, intrest_min,intrest_max)

	#newsa.compress(np.all(newsa == 0, axis = 0),axis = 1)
	#newsa[~(newsa==0).all(1)] #should work
	#newsa[~np.all(newsa == 0, axis=1)]#should work
	#print(newsa.shape)
	
	plt.pcolor(yt, zt, newsa,cmap='RdBu',vmin=0, vmax=1)	
	plt.title('if in region or not plot'+str(intrest_min)+'to'+str(intrest_max))
	
	#plt.title('The pcolor plot of dy dz and salinity')
	plt.axis([yt.min(), yt.max(), zt.min(), zt.max()])
	plt.colorbar()
	plt.gca().invert_yaxis()





	plt.subplot(2, 2, 2)
	sa_bf = np.array(sa2dyz) #salinity before arraylize


	intrest_min = 35.1
	intrest_max = 36.5
	#call function
	#print(sa_bf.shape)
	newsa = effectionPlot(sa_bf, intrest_min,intrest_max)

	plt.pcolor(yt, zt, newsa,cmap='RdBu',vmin=0, vmax=1)	
	plt.title('if in region or not plot'+str(intrest_min)+'to'+str(intrest_max))

	plt.axis([yt.min(), yt.max(), zt.min(), zt.max()])
	plt.colorbar()
	plt.gca().invert_yaxis()













	plt.subplots_adjust(wspace=0.5, hspace=0.5)
	plt.show()



	#set as length of 0 index cause I know each line is same dimension
	#z = [(newsa[x] == newsa[x+1]) for x in range(0, len(newsa[0])-1)]
	#if False in z:
		#not all equal => not all 0 => keep it
	#else:

def checkEqual1(iterator):
	iterator = iter(iterator)
	try:
		first = next(iterator)
	except StopIteration:
		return True
	return all(first == rest for rest in iterator)

