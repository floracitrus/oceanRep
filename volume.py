import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy

#My functions
def printStatus(matrix):
	print("shapes of Matrix")
	print(matrix.shape)
	#print("xt  ||yt  ||zt  ||sa  ||axy  ||ayz  ")
	#print(str(xt.shapes)+" || "+str(yt.shapes)+" || "+str(zt.shapes)+" || "+str(sa.shapes)+" || "+str(axy.shapes)+" || "+str(ayz.shapes)+" ")

def maskMatrix(matrix, rangeA, rangeB):
	np.errstate(invalid='ignore')
	m = (matrix>=rangeA) & (matrix<rangeB) 

	#selected = matrix[m] #a list of selected points
	return m

with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	#list of variables 
	#print(list(file.keys()))
	xxt = list(file['xt']) #360
	yyt = list(file['yt']) #180
	ssa = list(file['SA']) #12x101x180x360
	zzt = list(file['zt'])
	aaxy = list(file['Axy']) #101x180x360
	aayz = list(file['Ayz']) #101x180x360
	aaxz = list(file['Axz']) #101x180x360
	
	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)
	zt = np.squeeze(zzt)

	sa  = np.squeeze(ssa)
	axy = np.squeeze(aaxy)
	ayz = np.squeeze(aayz)


	#printStatus(xt)
	#printStatus(sa3d)
	printStatus(axy)


	#fixed Janurary for sa
	sa3d = np.squeeze(sa[0, :, :, :])
	#fixed longtitude at 215
	sa2d = np.squeeze(sa3d[:,:,215])
	
	sa2ds = np.squeeze(sa3d[0,:,:])
	#area of surface layer
	axy2d = np.squeeze(axy[0,:,:])
	#area of cross-section
	ayz2d = np.squeeze(ayz[:,:,215])



################## The sum of x(in360) for y-z layer ###################
################## useful? waiting for check         ###################
#
#
#	gridy, gridz = np.meshgrid(yt,zt)
#	print(type(gridy))
#	mask = maskMatrix(sa3d, 34.4, 34.5)
#	xx = np.sum(mask, axis = 2)
#	print("xx"+str(xx.shape))
#
#	plt.figure()
#	plt.imshow(xx)# extent = [0,1,0,1])# hor_min, hor_max, ver_min, ver_max
#	#plt.imshow(xx, extent=[0, 1, 0, 1])
#	plt.show()
###########################################################################


################## Plot the truth graph with given range###################
#A shoe shape figure

	gridy, gridz = np.meshgrid(yt,zt)
	print(type(gridy))
	m = maskMatrix(sa2d, 34.4, 34.5)
	mask = m & (gridy<0) #gridy<0 to filter out the positive axis
	plt.figure()
	plt.imshow(mask)
	plt.show()

###########################################################################


################## the add on map with salinity contour ###################

	gridx, gridy = np.meshgrid(xt,yt)
	print(sa2ds.shape)
#---------------------------------------------------------------------------
#world-map-base	
	# plt.imshow(sa2ds,extent=[xt.min(), xt.max(), yt.min(), yt.max()],
 #        interpolation='nearest', origin='lower')

	# plt.colorbar()
	# plt.plot()
	
#add-on contour
	# levels = [34.4,34.5]
	# plt.contourf(xt, yt, sa2ds, levels, colors = 'k')
	# #c = plt.contour(xt,yt,sa2ds,50,colors = 'k')
	# plt.plot()
	# plt.show()

#---------------------------------------------------------------------------
#the only contour part of add on testing different methods
	plt.subplot(2,2,1)
	levels = [34.4,34.5]
	plt.contourf(xt, yt, sa2ds, levels, colors = 'k')
	plt.title('34.4-34.5 contourf plot surface salinity')

	plt.subplot(2,2,2)
	c = plt.contour(xt,yt,sa2ds,100,colors = 'k')
	plt.title('contourf plot surface salinity 100')

	plt.subplot(2,2,3)
	m = maskMatrix(sa2ds, 33, 34.5)
	c = plt.contour(xt,yt,m,100,colors = 'k')
	plt.title('33-34.5 contour plot surface salinity 100')

	plt.subplot(2,2,4)
	m = maskMatrix(sa2ds, 34, 34.5)
	plt.title('34-34.5 contour plot surface salinity 50')
	c = plt.contour(xt,yt,m,50,colors = 'k')


	plt.show()

###########################################################################
###calculate the shaded area around antarctic on surface #############
###calculate volume between 20-80
	#iterate each depth of surface layer with salinity 34-34.5
	vol = 0 
	rangeA = 34.4
	rangeB = 34.5

	level = 100
	
	latitudeA = -20
	latitudeB = -80
	
	plt.title(str(rangeA)+' '+str(rangeB)+' salinity contour plot surface with selected in '+str(latitudeA)+' '+str(latitudeB))
	m = maskMatrix(sa2ds, rangeA, rangeB)
	mask = m & ((gridy<(-20)) & (gridy>(-80)))
	plt.contour(xt,yt,mask,level,colors = 'k')
	plt.plot()


	for i in [0,100]:#range zt
		sa2ds = np.squeeze(sa3d[i,:,:])
		m = maskMatrix(sa2ds, rangeA, rangeB)
		mask = m & ((gridy<(-20)) & (gridy>(-80)))
		a = axy2d[mask]
		vol += sum(a)

	print(vol) #4.36806369659e+13 at around -50+- contour
	plt.show()

###########################################################################













# Ayz2d       = squeeze(Ayz(216,:,:))';
# SA2d        = squeeze(SA(216,:,:))';
# [yt2d,zt2d] = meshgrid(yt,zt);
# index       = and(and(SA2d>=34.4, SA2d<34.5),yt2d<0);
# index       = and(SA>=34.4, SA<34.5);
# xx          = sum(index,3);
 
# figure
# imagesc(xx')
# set(gca,'YDir','normal')
 
# SA2d(index)
# sum(Ayz2d(index))
 
# figure
# imagesc(yt,zt,index)
# axis tight
 
# close all
 
# figure
# pcolor(xt,yt,squeeze(SA(:,:,1))'); shading flat
# set(gca,'YDir','normal')
# caxis([34.5 35])
# axis tight
 
# figure
# pcolor(xt,yt,squeeze(SA(:,:,1))'); shading flat
# %set(gca,'YDir','normal')
# caxis([30 37])
# axis tight
# colormap('bone')
# colorbar




