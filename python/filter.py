#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

mlp.rcParams['axes.linewidth'] = 2

# Characteristics of the passive elements
C = 0.0000001 # Farad
R = 100000    # Ohm

# Omega_0 (1/2) - Corner frequency
omega0C = 1./R/C

def fHighPassC(omega):
    rSquare = omega*omega/omega0C/omega0C
    return 1.0/(np.sqrt(1.0+1.0/rSquare))

# define values for normalized frequency
omegas = np.arange(0.0, 100000.0, 1)

# define the figure
plt.figure(1)

# double log plot
plt.loglog(omegas,fHighPassC(omegas),'g',linewidth=2.8)

# make plot nicer
plt.ylim((0.01,1))
plt.xlabel('frequency', fontsize=28)
plt.ylabel('attenuation', fontsize=28)
plt.legend(loc=0, fontsize=24)

ax = plt.gca()
ax.tick_params(axis='both', which='major', labelsize=20)
ax.grid(True,ls='--', lw=0.4, zorder=-99, color='gray', alpha=0.7,
        axis='y', which='both')
ax.grid(True,ls='--', lw=0.4, zorder=-99, color='gray', alpha=0.7,
        axis='x', which='major')

# save plot for later viewing
plt.savefig("highPassCFilter.png",bbox_inches='tight',dpi=400)
