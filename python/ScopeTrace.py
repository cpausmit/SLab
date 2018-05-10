#---------------------------------------------------------------------------------------------------
# C L A S S E S
#---------------------------------------------------------------------------------------------------
class ScopeTrace:
    """
    Class to mange a full scope trace.
    """
    undefined_value = -9999999

    def __init__(self,data,n_average=1):
        # data record
        self.data = data
        self.n_average = n_average
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
            f = line.split(',')
            if len(f)<5:
                continue
            
            x += float(i)
            y += float(f[4])+self.vertical_offset
            n += 1
            if n>n_average:
                self.xvalues.append(x/n)
                self.yvalues.append(y/n)
                n = 0
                x = 0
                y = 0
            i += 1
            
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
            baseline = sum/n
            jitter = abs(sum2 - 2*baseline*sum + baseline*baseline)/n

        return (baseline,jitter)

    def find_number_of_pulses(self,baseline,threshold,delta_min):
        n_pulses_found = 0
        last_y = self.yvalues[0]
        latched = False
        for y in self.yvalues:
            delta_y = last_y - y
            if   y<baseline-threshold:
                print " D: %f,  Dmin: %f"%(delta_y,delta_min)
                if delta_y>delta_min and not latched:
                    n_pulses_found += 1
                    latched = True
            elif y>baseline-threshold-delta_min:
                latched = False
            last_y = y

                
        return n_pulses_found 
