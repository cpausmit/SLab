#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['axes.linewidth'] = 2

def fHighPass(rw):
    result = 1.0/(np.sqrt(1.0+1.0/rw/rw))
    return result

# define values for normalized frequency
rws = np.arange(0.0, 100000.0, 1)

# define the figure
plt.figure(1)

# double log plot
plt.loglog(rws, fHighPass(rws), 'g', linewidth=2.8)

# set an axis limit on y axis
plt.ylim((0.01,1))

# fine tuning the axes
ax = plt.gca()
ax.tick_params(axis='both', which='major', labelsize=20)
ax.grid(True,ls='--',lw=0.4,zorder=-99,color='gray',alpha=0.7,axis='y',which='both')
ax.grid(True,ls='--',lw=0.4,zorder=-99,color='gray',alpha=0.7,axis='x', which='major')

plt.xlabel('normalized frequency',   fontsize=28)
plt.ylabel('attenuation', fontsize=28)
plt.legend(loc=0, fontsize=24)

plt.savefig("bodeHighPass.png",bbox_inches='tight',dpi=400)
