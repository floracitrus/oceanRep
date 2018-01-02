import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math

<<<<<<< HEAD
# [ -4.94673916   0.403058494  -4.21777040  -7.44140770
#   -5.00618925   6.75940917  -7.48810918  -4.04957492
#   -1.44372925   0.668968322  -5.76303070  -3.92261831]


with h5py.File('WOA_gsw_JMcD95_plus.mat', 'r') as file:
	xxt = list(file['xt']) #360
	yyt = list(file['yt']) #180
	ssa = list(file['SA']) #12x101x180x360
	sa  = np.squeeze(ssa)

	xt = np.squeeze(xxt)
	yt = np.squeeze(yyt)

	
	gridx, gridy = np.meshgrid(xt,yt)
	plt.subplot(1,2,1)
	plt.imshow(np.squeeze(sa[0,0,:,:]), extent=[xt.min(), xt.max(), yt.min(), yt.max()],cmap = 'PRGn', vmin = 32,vmax = 38,interpolation='nearest', origin='lower')
	plt.colorbar()
	plt.subplot(1,2,2)
	plt.imshow(np.squeeze(sa[7,0,:,:]), extent=[xt.min(), xt.max(), yt.min(), yt.max()], cmap='seismic',vmin = 32,vmax = 38,interpolation='nearest', origin='lower')
	plt.colorbar()
	plt.show()
=======
volList = [-652663.169149,-746266.288002,-711537.604518,-733834.16875,-915989.792616,-734469.03343,-764119.198171,-704553.574485,-794743.330259,-615978.965556,-805162.564102,-823308.161848]
plt.figure(1)
x = range(1,13)
rects1 = plt.bar(x,volList)
plt.show()
>>>>>>> 79be1bc5a1105c7ba61d549a7c51bfb6e71ea3a9
