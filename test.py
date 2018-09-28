import numpy as np
import main
#
#salary = 100000
#
#expenses = 50000
#
## Func
#def loopDed(ded):
#    ded = 0
#    while True:    
#        taxes = (salary - ded) * 0.25
#        gross = salary - taxes
#        
#        tempDed = gross - expenses
#        
#        if tempDed <= 0:
#            break
#        
#        diff = abs(tempDed - ded) / tempDed
#        
#        totalTempDed = [tempDed,ded]
#        ded = tempDed    
#        
#        if diff < 0.01:
#            totalTempDed = np.average(totalTempDed)
#            totalTempDed = np.round(totalTempDed/100)*100
#            
#            ded = totalTempDed
#            return ded
#            break
#
#charity = 0
#print(loopDed(charity))

a = np.arange(12).reshape((4,3))
print(a)

b = np.sum(a,axis=0)
print(b)