import h5py
import matplotlib.pyplot as plt
import numpy as np
from copy import copy, deepcopy
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import math

volList = [-652663.169149,-746266.288002,-711537.604518,-733834.16875,-915989.792616,-734469.03343,-764119.198171,-704553.574485,-794743.330259,-615978.965556,-805162.564102,-823308.161848]
plt.figure(1)
x = range(1,13)
rects1 = plt.bar(x,volList)
plt.show()