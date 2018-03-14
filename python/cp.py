#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

# initial settings
mlp.rcParams['axes.linewidth'] = 2

with open("cp-water.dat","r") as file:
    data = file.read()

print data

temps = []
cpws = []
for line in data.split("\n"):
    f = line.split(',')
    if len(f)>1:
        temps.append(float(f[0]))
        cpws.append(float(f[1]) * 1000.) # convert from kJ/(kg K) to J/(kg K)

# define the figure
plt.figure(1)
plt.plot(temps,cpws)

# make plot nicer
plt.xlabel('Temperature [C]', fontsize=28)
plt.ylabel('cp water [J/(kg K)]', fontsize=28)

# save plot for later viewing
#plt.show()
plt.savefig("cp-water.png",bbox_inches='tight',dpi=400)
