## Total Savings/Investments
import main
import allocations as al

import numpy as np
import random as rand
import matplotlib.pyplot as plt

loopLen = 1
earningsAlloc = np.zeros((loopLen,years,len(al.allocations)))

#0) hiDiv
#1) ltLowVol
#2) largeCap
#3) stHiVol

#4) retRoth401
#5) retTrad401
#6) col529

#7) emergFunds
#8) medTerm
#9) shortTerm
#10) excSpend

def allocations(years):
    for n in range(years):
        for m in range(len(al.allocations)):
            if m == 0:
                earningsAlloc[n,m] = rand.normalvariate(4.0,0.5)
            elif m == 1:
                earningsAlloc[n,m] = rand.normalvariate(8.0,2.5)
            elif m == 2:
                earningsAlloc[n,m] = rand.normalvariate(12.0,4.5)
            elif m == 3:
                earningsAlloc[n,m] = rand.normalvariate(16.0,8.0)
                if earningsAlloc[n,m] > 30:
                    earningsAlloc[n,m] = 30
            elif m == 4 or m == 5:
                mu = np.zeros((years,1))
                sigma = np.zeros((years,1))
                
                muStart = 7.0
                muEnd = 4.0
                
                mu[n] = muStart - ((n / years) * (muStart - muEnd))
                sigma[n] = 0.25 * mu[n]
                
                earningsAlloc[n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 6:
                mu = np.zeros((years,1))
                sigma = np.zeros((years,1))
                
                muStart = 7.0
                muEnd = 5.0
                
                mu[n] = muStart - ((n / years) * (muStart - muEnd))
                sigma[n] = 0.35 * mu[n]
                
                earningsAlloc[n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 7:
                earningsAlloc[n,m] = 0.05
            elif m == 8:
                earningsAlloc[n,m] = 1.95
            elif m == 9:
                earningsAlloc[n,m] = 1.0
            elif m == 10:
                earningsAlloc[n,m] = 0
            
    earningsAlloc = earningsAlloc / 100
    meanEarningsAlloc = np.mean(earningsAlloc,axis = 0)

#print(meanEarningsAlloc)

#plt.clf()
#plt.plot(meanEarningsAlloc)