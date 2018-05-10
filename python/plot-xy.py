#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp

from optparse import OptionParser

# initial settings
mlp.rcParams['axes.linewidth'] = 2

#---------------------------------------------------------------------------------------------------
def readDataFromFile(name): 

    with open(name+".dat","r") as file:
        data = file.read()
        
    xs = []
    ys = []
    for line in data.split("\n"):
        f = line.split(',')
        if len(f)>1:
            xs.append(float(f[0]))
            ys.append(float(f[1]))

    return (xs,ys)

#---------------------------------------------------------------------------------------------------
# define and get all command line arguments
parser = OptionParser()
parser.add_option("-n", "--name",  dest="name",  default='temp',                help="name of plot")
parser.add_option("-x", "--xtitle",dest="xtitle",default='Time [milli seconds]',help="x axis title")
parser.add_option("-y", "--ytitle",dest="ytitle",default='analog values',       help="y axis title")
(options, args) = parser.parse_args()

# get my data
(xs,ys) = readDataFromFile(options.name)

# define the figure
plt.figure(1)
plt.plot(xs,ys)

# make plot nicer
plt.xlabel(options.xtitle, fontsize=28)
plt.ylabel(options.ytitle, fontsize=28)

# save plot for later viewing
plt.savefig(options.name+".png",bbox_inches='tight',dpi=400)
