#---------------------------------------------------------------------------------------------------
# C L A S S E S
#---------------------------------------------------------------------------------------------------
import math

class ScopeTrace:
    """
    Class to mange a full scope trace.
    """
    undefined_value = -9999999

    def __init__(self,data,n_average=1):
        # data record
        self.data = data
        self.n_average = n_average
        self.reading_error = 0
        # get the oscilloscope setup
        self.record_length = self.find_value('Record Length',data)
        self.sample_interval = self.find_value('Sample Interval',data)
        self.trigger_point =  self.find_value('Trigger Point',data)
        self.vertical_units = self.find_value('Vertical Units',data,'str')
        self.vertical_scale = self.find_value('Vertical Scale',data)
        self.vertical_offset = self.find_value('Vertical Offset',data)
        self.horizontal_units = self.find_value('Horizontal Units',data,'str')
        self.source = self.find_value('Source',data,'str')

        # get the scopes raw readings (average as many as you want)
        x = 0
        y = 0
        i = 0
        n = 0
        self.xvalues = []
        self.yvalues = []
        for line in data.split("\n"):

            try:
                f = line.split(',')
                if len(f)<5:
                    print ' Skipping line: %s'%line
                    continue
                
                x += float(i)
                y += float(f[4])+self.vertical_offset
                n += 1
                if n>=n_average:
                    self.xvalues.append(x/n)
                    self.yvalues.append(y/n)
                    n = 0
                    x = 0
                    y = 0
                i += 1
            except:
                print ' ERROR - reading file: '+ line
                self.reading_error += 1
            
    def find_value(self,name,data,type="f"):
        value = self.undefined_value
        for line in data.split("\n"):
            f = line.split(',')
            if f[0] == name:
                if   type == 'f':
                    value = float(f[1])
                    #print " Value[%s]  %f (F)"%(name,value)
                elif type == 'i':
                    value = int(f[1])
                    #print " Value[%s]  %d (I)"%(name,value)
                else:
                    value = f[1]
                    #print " Value[%s]  %s (S)"%(name,value)
                break
        return value

    def find_baseline_and_jitter(self,xmin,xmax):
        n = 0
        sum = 0
        sum2 = 0
        for x,y in zip(self.xvalues,self.yvalues):
            if x>xmin and x<xmax:
                n = n + 1
                sum = sum + y
                sum2 = sum2 + y*y

        baseline = 0
        jitter = 0
        if n>0:
            baseline = sum/float(n)
            jitter = math.sqrt(sum2/float(n) - baseline*baseline)
            
            #jitter = abs(sum2 - 2.0*baseline*sum + baseline*baseline)/float(n)

        return (baseline,jitter)

    def find_number_of_pulses(self,baseline,threshold,delta_min):
        n_pulses_found = 0
        last_y = self.yvalues[0]
        latched = False
        for y in self.yvalues:
            delta_y = last_y - y
            if   y<baseline-threshold:
                if delta_y>delta_min and not latched:
                    n_pulses_found += 1
                    latched = True
            elif y>baseline-threshold-delta_min:
                latched = False
            last_y = y

                
        return n_pulses_found 

    def inverted(self):
	baseline = self.find_baseline_and_jitter(self.xvalues[0], self.trigger_point)[0]
	return [-(val-baseline) for val in self.yvalues]

    def reset_adcs(self):
	self.yvalues = [0 for val in self.yvalues]
	return
    
    def add_adcs(self,yvalues,invert=False):
        for i in range(0,len(yvalues)):
            if invert:
                self.yvalues[i] -= yvalues[i]
            else:
	        self.yvalues[i] += yvalues[i]
	return 

    def write_trace(self,file_name):
        with open(file_name,"w") as fh:
            i = 0
            for x,y in zip(self.xvalues,self.yvalues):
                if   i==0:
                    s = "Record Length, %s,"%str(self.record_length)
                elif i==1:
                    s = "Sample Interval,%s,"%str(self.sample_interval)
                elif i==2:
                    s = "Trigger Point,%s,"%str(self.trigger_point)
                elif i==3:
                    s = "Vertical Units,%s,"%self.vertical_units
                elif i==4:
                    s = "Vertical Scale,%s,"%str(self.vertical_scale)
                elif i==5:
                    s = "Vertical Offset,%s,"%str(self.vertical_offset)
                elif i==6:
                    s = "Horizontal Units,%s,"%self.horizontal_units
                elif i==7:
                    s = "Source,%s,"%self.source
                else:
                    s = ",,"
                fh.write("%s,%f,%f,\n"%(s,x,y-self.vertical_offset))

                i += 1
