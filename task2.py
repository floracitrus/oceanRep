import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

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
#for bar chart
def autolabel(rects):
		for rect in rects:
			height = rect.get_height()
			plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height), ha='center', va='bottom')

# def cube_marginals(cube, normalize=False):
# 	c_fcn = np.mean if normalize else np.sum
# 	xy = c_fcn(cube, axis=0)
# 	xz = c_fcn(cube, axis=1)
# 	yz = c_fcn(cube, axis=2)
# 	return(xy,xz,yz)

with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
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


################# graph of each month surface salinity ##########################
#world salinity map
	# c = plt.contour(xt,yt,np.squeeze(sa[0, 0, :, :]),100,colors = 'k')
	# plt.clabel(c, inline=2, fontsize=10)
	# plt.plot()
	# plt.show()
	#35.55-36.15
#from the picture we can see that it around 35.9-36 larger region will be 35.6-36.1
#so we applied a mask1
	# m = maskMatrix(np.squeeze(sa[0, 0, :, :]), 35.6, 36.1)
	# d = plt.contour(xt, yt, m, 1 ,colors = 'k')
	# plt.clabel(d, inline = 1, fontsize = 10)
	# plt.title("January surface with sal 35.6-36.1")
	# plt.plot()
	# plt.show()

#another range of mask2 
	# plt.figure()
	# for i in range(0, 11):
	# 	m = maskMatrix(np.squeeze(sa[i, 0, :, :]), 36.0, 36.2)
	# 	plt.subplot(3,4,i+1)
	# 	plt.imshow(m, extent=[xt.min(), xt.max(), yt.min(), yt.max()], interpolation='nearest', origin='lower')
	# 	plt.title("monthly "+str(i+1)+"surf Sa")
	# 	#plt.plot()

	# plt.show()

	# for i in range(0,11):
	# 	saMonth = np.squeeze(sa[i, 0, :, :])
	# 	plt.subplot(4,4,i+1)
	# 	c = plt.contour(xt,yt,saMonth,100,colors = 'k')
	# 	plt.clabel(c, inline=1, fontsize=10)
	# 	plt.title(i)
	# plt.show()


	# plt.figure(2)
	# gridx, gridy = np.meshgrid(xt,yt)
	# for i in range(0, 12):

	# 	m = maskMatrix(np.squeeze(sa[i, 0, :, :]), 36.0, 36.2)
	# 	mask = m & ((gridx<280) & (gridx>200))
	# 	circleOnly = mask & (gridy<0)
	# 	plt.subplot(3,4,i+1)
	# 	plt.imshow(circleOnly, extent=[xt.min(), xt.max(), yt.min(), yt.max()], interpolation='nearest', origin='lower')
	# 	plt.title("monthly "+str(i+1)+"surf Sa")
	# 	#plt.plot()

	# plt.show()


##################################################################################
	
	plt.figure(1)
	gridx, gridy = np.meshgrid(xt,yt)
	volList = []#the monthly volList
	for i in range(0, 12):
		vol = 0
		for j in range(101):#range zt 0-100
			m = maskMatrix(np.squeeze(sa[i, j, :, :]), 36.0, 36.2)
			m = m & (((gridx<280) & (gridx>200)) & (gridy<0))
			axy2d = np.squeeze(axy[j,:,:])#each layer in z direction
			a = axy2d[m]
			# print("this is mask m")
			# print(m)#m is a true-false matrix
			# print("this is a")
			# print(a)#a is the true-false value put into area
			vol += sum(a)
		volList.append(vol)

	#plt.plot(volList)
	#x = range(1,13)
	x = range(0,12)
	rects1 = plt.bar(x,volList)
	plt.title("volume of certain region monthly graph")
	plt.ylabel('volume of the circle')
	plt.xlabel('Month')
	#plt.xlim(1, 12)
	
	#autolabel(rects1)

	
	
	plt.figure(2)
	plt.title("volume of certain region changes graph")
	diffVolList = np.diff(volList)
	plt.plot(diffVolList)
	

#############the 3d surface salinity ###################
	fig = plt.figure(3)
	ax = fig.gca(projection='3d')

	# Make data.
	X, Y = np.meshgrid(xt,yt)
	Z = np.squeeze(sa[0,0,:,:])
	# Plot the surface.
	surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
						   linewidth=0, antialiased=False)

	# Customize the z axis.
	#ax.set_zlim(-1.01, 1.01)
	plt.title("salinity 3d plot surface")
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

	# Add a color bar which maps values to colors.
	fig.colorbar(surf, shrink=0.5)

################################
	# plt.figure(4)
	# #plt.title('surface salinity over the year')
	# for i in range(12):
	# 	plt.subplot(3,4,i+1)
	# 	c = plt.contour(xt,yt,np.squeeze(sa[i,0,:,:]),100,colors='k')
	# 	plt.clabel(c, inline=1, fontsize=10)
##################################
	i = 0
	plt.figure(5)
	plt.subplot(3,3,1)
	#January surface xy layer
	plt.imshow(np.squeeze(sa[i,0,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("surface Layer January")
	plt.colorbar()
	
	plt.subplot(3,3,2)
	plt.imshow(np.squeeze(sa[i,10,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 50m Layer")
	

	plt.subplot(3,3,3)
	plt.imshow(np.squeeze(sa[i,20,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 100m Layer")
	

	plt.subplot(3,3,4)
	plt.imshow(np.squeeze(sa[i,21,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 125m Layer")
	
	plt.subplot(3,3,5)
	plt.imshow(np.squeeze(sa[i,22,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 150m Layer")
	

	plt.subplot(3,3,6)
	plt.imshow(np.squeeze(sa[i,23,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 175m Layer")
	plt.colorbar()
	#January depth60 xy layer

	plt.subplot(3,3,7)
	plt.imshow(np.squeeze(sa[i,24,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 200m Layer")
	plt.colorbar()


	plt.subplot(3,3,8)
	plt.imshow(np.squeeze(sa[i,25,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 225 Layer")
	
	#January depth100 xy layer
	plt.subplot(3,3,9)
	plt.imshow(np.squeeze(sa[i,56,:,:]),extent=[xt.min(), xt.max(), yt.min(), yt.max()],
		 interpolation='nearest', origin='lower',cmap=plt.cm.coolwarm,vmin = 35.9, vmax = 36.3)
	plt.title("depth 1000 Layer")
	
###########################################################


	plt.figure(6)
	plt.subplot(2,2,1)
	plt.pcolor(yt, zt,np.squeeze(sa[0,:,:,212]),cmap=plt.cm.rainbow ,vmin=35.9, vmax=36.3)	
	plt.axis([yt.min(), yt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("longtitude 212 January")
	plt.gca().invert_yaxis()

	plt.subplot(2,2,2)
	plt.pcolor(yt, zt,np.squeeze(sa[0,:,:,222]),cmap=plt.cm.rainbow,vmin=35.9, vmax=36.3)	
	plt.axis([yt.min(), yt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("longtitude 222")
	plt.gca().invert_yaxis()


	plt.subplot(2,2,3)
	plt.pcolor(yt, zt,np.squeeze(sa[0,:,:,235]),cmap=plt.cm.rainbow,vmin=35.9, vmax=36.3)	
	plt.axis([yt.min(), yt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("longtitude 235")
	plt.gca().invert_yaxis()

	plt.subplot(2,2,4)
	plt.pcolor(yt, zt,np.squeeze(sa[0,:,:,245]),cmap=plt.cm.rainbow,vmin=35.9, vmax=36.3)	
	plt.axis([yt.min(), yt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("longtitude 245")
	plt.gca().invert_yaxis()
####################################################
	plt.figure(7)
	plt.subplot(2,2,1)
	plt.pcolor(xt,zt,np.squeeze(sa[0,:,-10,:]),cmap=plt.cm.Spectral ,vmin=35, vmax=36.5)	
	plt.axis([xt.min(), xt.max(), zt.min(), zt.max()])
	plt.colorbar()
	plt.title("latitude -10 January")
	plt.gca().invert_yaxis()

	plt.subplot(2,2,2)
	plt.pcolor(xt, zt,np.squeeze(sa[0,:,-15,:]),cmap=plt.cm.Spectral,vmin=35, vmax=36.5)	
	plt.axis([xt.min(), xt.max(), zt.min(),zt.max()])
	plt.colorbar()
	plt.title("latitude -15")
	plt.gca().invert_yaxis()


	plt.subplot(2,2,3)
	plt.pcolor(xt,zt,np.squeeze(sa[0,:,-16,:]),cmap=plt.cm.Spectral,vmin=35, vmax=36.5)	
	plt.axis([xt.min(), xt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("latitude -16")
	plt.gca().invert_yaxis()

	plt.subplot(2,2,4)
	plt.pcolor(xt,zt,np.squeeze(sa[0,:,-17,:]),cmap=plt.cm.Spectral,vmin=35, vmax=36.5)	
	plt.axis([xt.min(), xt.max(), zt.min(), 400])
	plt.colorbar()
	plt.title("latitude -17")
	plt.gca().invert_yaxis()
	
####################################################

	# cube = np.squeeze(sa[0,:,:,:])
	# (Z,Y,X) = cube.shape
	# plot_front = True
	# x = xt
	# y = yt
	# z = zt
	# (xy,xz,yz) = cube_marginals(cube,normalize=False)
	
	# fig = plt.figure(8)
	# ax = fig.gca(projection='3d')

	# volume = np.squeeze(sa[0,:,:,:])

	# # Create the x, y, and z coordinate arrays.  We use 
	# # numpy's broadcasting to do all the hard work for us.
	# # We could shorten this even more by using np.meshgrid.
	# x = np.arange(volume.shape[0])[:, None, None]
	# y = np.arange(volume.shape[1])[None, :, None]
	# z = np.arange(volume.shape[2])[None, None, :]
	# x, y, z = np.broadcast_arrays(x, y, z)

	# # Turn the volumetric data into an RGB array that's
	# # just grayscale.  There might be better ways to make
	# # ax.scatter happy.
	# c = np.tile(volume.ravel()[:, None], [1, 3])

	# # Do the plotting in a single call.
	# fig = plt.figure()
	# ax = fig.gca(projection='3d')
	# ax.scatter(x.ravel(),
	#            y.ravel(),
	#            z.ravel(),
	#            c=c)


	# # draw edge marginal surfaces
	# offsets = (Z-1,0,X-1) if plot_front else (0, Y-1, 0)
	# cset = ax.contourf(x[None,:].repeat(Y,axis=0), y[:,None].repeat(X,axis=1), xy, zdir='z', offset=offsets[0], cmap=plt.cm.coolwarm, alpha=0.75)
	# cset = ax.contourf(x[None,:].repeat(Z,axis=0), xz, z[:,None].repeat(X,axis=1), zdir='y', offset=offsets[1], cmap=plt.cm.coolwarm, alpha=0.75)
	# cset = ax.contourf(yz, y[None,:].repeat(Z,axis=0), z[:,None].repeat(Y,axis=1), zdir='x', offset=offsets[2], cmap=plt.cm.coolwarm, alpha=0.75)

	# # draw wire cube to aid visualization
	# ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[0,0,0,0,0],'k-')
	# ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[Z-1,Z-1,Z-1,Z-1,Z-1],'k-')
	# ax.plot([0,0],[0,0],[0,Z-1],'k-')
	# ax.plot([X-1,X-1],[0,0],[0,Z-1],'k-')
	# ax.plot([X-1,X-1],[Y-1,Y-1],[0,Z-1],'k-')
	# ax.plot([0,0],[Y-1,Y-1],[0,Z-1],'k-')

	# ax.set_xlabel('X')
	# ax.set_ylabel('Y')
	# ax.set_zlabel('Z')
	
	plt.show()
