import numpy as np

def negExpGrowth(rng,iterate=10): 
    base = 0.0
    chng = 0.01
    
    x = np.arange(rng)
    y = ((-(1+base)**x + 1) / 100) + 1
    
    diff = abs(y[-1]-0)
    
    for n in range(iterate):
        while True:
            negBase = base - chng
            y = ((-(1+negBase)**x + 1) / 100) + 1
            negDiff = abs(y[-1]-0)
            
            posBase = base + chng
            y = ((-(1+posBase)**x + 1) / 100) + 1
            posDiff = abs(y[-1]-0)
            
            newDiff = posDiff if posDiff < negDiff else negDiff
            
            if newDiff < diff:
                base = posBase if posDiff < negDiff else negBase
                diff = newDiff
                continue
            else:
                break
            
        chng = chng / 10