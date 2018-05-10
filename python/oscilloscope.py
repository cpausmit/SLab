#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
import ScopeTrace

#---------------------------------------------------------------------------------------------------
# M A I N
#---------------------------------------------------------------------------------------------------
# initial settings
mlp.rcParams['axes.linewidth'] = 2

filename = sys.argv[1]
print ' File to open: ' + filename
with open(filename,"r") as file:
    data = file.read()

# decode the scope trace
trace = ScopeTrace.ScopeTrace(data,8)

# find basline and jitter
baseline,jitter = trace.find_baseline_and_jitter(0,250)

threshold = 3*jitter
delta_min = 2*jitter
n_pulses = trace.find_number_of_pulses(baseline,threshold,delta_min)

print ' Baseline: %10.6f,  Jitter: %10.6f,  Npulses: %d'%(baseline,jitter,n_pulses)

# get x and y values of the traces
recs = trace.xvalues
adcs = trace.yvalues

# define the figure
fig = mlp.pyplot.gcf()
fig.set_size_inches(18.5, 14.5)
plt.figure(1)
plt.plot(recs,adcs)

# draw horizontal
#plt.plot([0,0.04],[2500,0.04],'k-')
plt.axhline(y=baseline,                     color='b', linestyle='-', linewidth=4)
plt.axhline(y=baseline-threshold+delta_min, color='g', linestyle='-')
plt.axhline(y=baseline-threshold,           color='r', linestyle='-')
plt.axhline(y=baseline-threshold-delta_min, color='g', linestyle='-')

# make plot nicer
plt.xlabel('x-interval [n%s]'%trace.horizontal_units, fontsize=28)
plt.ylabel('y-reading [%s]'%trace.vertical_units, fontsize=28)

# tick marker sizes
ax = plt.gca()
ax.xaxis.set_tick_params(labelsize=16)
ax.yaxis.set_tick_params(labelsize=20)

ymin,ymax = ax.get_ylim()
dy = ymax-ymin
xmin,xmax = ax.get_xlim()
dx = xmax-xmin
plt.text(xmin-0.1*dx,ymin-0.1*dy, r'Source: %s'%(trace.source), fontsize=20)

# save plot for later viewing
plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)
plt.savefig("adcs.png",bbox_inches='tight',dpi=400)
plt.show()
