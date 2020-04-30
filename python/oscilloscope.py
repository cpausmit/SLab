#!/usr/bin/env python
import sys
import pylandau
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mlp
from scipy.optimize import curve_fit

import ScopeTrace

plotting = True
fitting = True
simulation = False
n_traces = 100
pulse_rate = 4.6

def digitize(mod,adcs):
    # digitize the input data with the given modifier
    for i in range(0,len(adcs)):
        adcs[i] = int(adcs[i]*mod)/float(mod)
    return adcs
    
def events_per_trace(n_traces,rate):
    # generate the number of pulses for a fixed number of traces (avoid bias due to limited total
    # number by generating 10 times the total)
    n_stat = 10.0 # just to avoid trouble for using all traces
    rnorms = np.random.uniform(0.0,n_traces*n_stat,int(n_traces*rate*n_stat))
    bins = np.linspace(0.0,n_traces*n_stat,int(n_traces*n_stat)+1)
    hist, bins = np.histogram(rnorms,bins=bins)
    return hist

def fit_pulse(trace):
    # fit the peak
    x_array = np.array(trace.xvalues)
    y_array = np.array(trace.inverted())
    idx = np.where(y_array == y_array.max())

    # if multiple x values of the same max y values, selects the first max
    idx = idx[0][0]
    x_values_peak = x_array[idx]
    mpv = x_array[idx]
    amp = y_array.max()
    eta = fwhm(x_array,y_array)
    landau_par, pcov_rmin = curve_fit(pylandau.landau, x_array, y_array, p0=(mpv, 1, amp))
    print landau_par

    plot_pulse(trace,baseline,threshold)
    plt.plot(x_array,mylandau(x_array, landau_par[0], landau_par[1], landau_par[2]), label='Landau Fit')
    plt.show()

    return landau_par, pcov_rmin

def mylandau(xvals,peak,width,ampl):
    # transform the input to the landau and return the scaled values
    nxvals = np.array([])
    for xv in xvals:
        nxvals = np.append(nxvals,(xv-peak)/width)
    yvals = pylandau.landau(nxvals)
    return yvals * ampl

def fwhm(xvals,yvals):
    '''
    Returns an approximated full width at half maximum.
    '''
    idx = np.where(yvals == yvals.max())
    idx = idx[0][0]
    y_closest_to_hm = min(yvals, key=lambda x: abs(x - 0.5*max(yvals)))
    idx_hm_left = np.where(yvals == min(yvals[:idx], key=lambda x: abs(x-y_closest_to_hm)))
    idx_hm_right = np.where(yvals == min(yvals[idx:], key=lambda x: abs(x-y_closest_to_hm)))
    x_hm_left = xvals[idx_hm_left[0][0]]
    x_hm_right = xvals[idx_hm_right[0][0]]
    fw = abs(x_hm_left-x_hm_right)

    return fw

def plot_pulse(trace,baseline,threshold,delta_min=0,n_pulses=0):

    ## get x and y values of the traces
    recs = trace.xvalues
    adcs = trace.inverted()
    
    # define the figure
    fig = mlp.pyplot.gcf()
    fig.set_size_inches(18.5, 14.5)
    plt.figure(1)
    plt.plot(recs,adcs)
    
    # draw horizontal
    plt.axhline(y=0,                     color='b', linestyle='-', linewidth=2)
    plt.axhline(y=0+threshold+delta_min, color='g', linestyle='-')
    plt.axhline(y=0+threshold,           color='r', linestyle='-')
    plt.axhline(y=0+threshold-delta_min, color='g', linestyle='-')
    
    # make plot nicer
    plt.xlabel('x-trace [n%s]'%trace.horizontal_units, fontsize=28)
    plt.ylabel('y-reading [%s]'%trace.vertical_units, fontsize=28)
    
    # tick marker sizes
    ax = plt.gca()
    #ax.xaxis.set_tick_params(labelsize=16)
    #ax.yaxis.set_tick_params(labelsize=20)
    
    ymin,ymax = ax.get_ylim()
    dy = ymax-ymin
    xmin,xmax = ax.get_xlim()
    dx = xmax-xmin
    plt.text(xmin-0.1*dx,ymin-0.05*dy, r'Source:  %s'%(trace.source), fontsize=20)
    plt.text(xmin-0.1*dx,ymin-0.07*dy, r'#Pulses: %d'%(n_pulses), fontsize=20)
    
    # save plot for later viewing
    plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)
    #plt.savefig(filename+".png",bbox_inches='tight',dpi=400)
    #plt.show()

def plot_trace(trace):

    ## get x and y values of the traces
    recs = trace.xvalues
    adcs = trace.yvalues
    
    # define the figure
    fig = mlp.pyplot.gcf()
    fig.set_size_inches(18.5, 14.5)
    plt.figure(1)
    plt.plot(recs,adcs)

    # tick marker sizes
    ax = plt.gca()
    ax.xaxis.set_tick_params(labelsize=16)
    ax.yaxis.set_tick_params(labelsize=20)
    
    ymin,ymax = ax.get_ylim()
    dy = ymax-ymin
    xmin,xmax = ax.get_xlim()
    dx = xmax-xmin
    plt.text(xmin-0.1*dx,ymin-0.05*dy, r'Source:  %s'%(trace.source), fontsize=20)
    
    # save plot for later viewing
    plt.subplots_adjust(top=0.99, right=0.99, bottom=0.10, left=0.10)

def simulate_traces(trace,baseline,jitter,landau_par,n_traces,pulse_rate):
    # simulate a data full data sample

    # generate number of events per time trace (fixed pulse_rate --> Poisson)
    traces = events_per_trace(n_traces,pulse_rate)
    index = 0
    x_array = np.array(trace.xvalues)
    for ne in traces[0:n_traces]:
        print ne

        trace.reset_adcs()
        
        means = np.random.uniform(250,trace.xvalues[-1],ne)
        widths = np.random.normal(landau_par[1],0.05*landau_par[1],ne) 
        amps  = np.random.normal(40*jitter,10*jitter,ne)
        
        # add the core function (as fitted from the data)
        for m,w,a in zip(means,widths,amps):
            trace.add_adcs(mylandau(x_array,m,w,a),True)

        # finally add the baseline and the noise
        blj = digitize(500,(np.random.normal(baseline,jitter,len(trace.yvalues))).tolist())
        trace.add_adcs(blj)

        # find baseline and jitter
        b,j = trace.find_baseline_and_jitter(0,250)
        threshold = 5*jitter
        delta_min = 2*jitter
        n_pulses = trace.find_number_of_pulses(b,threshold,delta_min)
    
        file_name = "T%06d.csv"%index
        print ' Filename: %s,  Baseline: %10.6f,  Jitter: %10.6f,  Npulses: %d'\
        %(file_name,b,j,n_pulses)

        if plotting:
            plot_pulse(trace,baseline,threshold,delta_min,n_pulses)
            plt.show()

        trace.write_trace(file_name)
        index += 1

    
#---------------------------------------------------------------------------------------------------
# M A I N
#---------------------------------------------------------------------------------------------------
# initial settings
mlp.rcParams['axes.linewidth'] = 2

for filename in sys.argv[1:]:
    with open(filename,"r") as file:
        data = file.read()

    # decode the scope trace
    trace = ScopeTrace.ScopeTrace(data)
    x_array = np.array(trace.xvalues)
    if trace.reading_error>1 or len(trace.yvalues)<10:
        print " WARNING -- skipping this file has reading errors: %s"%(filename)
        continue
    
    # find baseline and jitter
    baseline,jitter = trace.find_baseline_and_jitter(0,250)
    
    threshold = 5*jitter
    delta_min = 2*jitter
    n_pulses = trace.find_number_of_pulses(baseline,threshold,delta_min)
    
    print ' Filename: %s,  Baseline: %10.6f,  Jitter: %10.6f,  Npulses: %d'\
        %(filename,baseline,jitter,n_pulses)

    if plotting:
        #plot_trace(trace)
        plot_pulse(trace,baseline,threshold,delta_min,n_pulses)
        plt.show()
        
    if fitting:
        landau_par, pcov_rmin = fit_pulse(trace)
        
    if simulation:
        # start with the orginal plot
        plot_trace(trace)
        # reset and simulate the 'same' pulse
        trace.reset_adcs()
        # add the core function (as fitted from the data)
        trace.add_adcs(mylandau(x_array, landau_par[0], landau_par[1], landau_par[2]),True)
        # add the basline and the noise
        blj = digitize(500,(np.random.normal(baseline,jitter,len(trace.yvalues))).tolist())
        trace.add_adcs(blj)
        trace.write_trace("%s--test"%filename)
        # plot the simulated plot on top
        plot_trace(trace)
        plt.show()
        # simulate a set number of traces with a given fixed pulse rate
        simulate_traces(trace,baseline,jitter,landau_par,n_traces,pulse_rate)
