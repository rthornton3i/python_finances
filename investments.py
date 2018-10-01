## Total Savings/Investments
import main
import allocations as al
import expenses as ex
import withholdings as wh

import numpy as np
import random as rand
import matplotlib.pyplot as plt

loopLen = 10
earningsAlloc = np.zeros((loopLen,main.years,len(al.allocations)))

#hiDiv
#ltLowVol
#largeCap
#stHiVol
#retRoth401
#retTrad401
#col529
#emergFunds
#medTerm
#shortTerm
#excSpend

for n in range(main.years):
    for m in range(len(al.allocations)):
        for i in range(loopLen):
            if m == 0:
                earningsAlloc[i,n,m] = rand.normalvariate(4.0,0.5)
            elif m == 1:
                earningsAlloc[i,n,m] = rand.normalvariate(8.0,2.5)
            elif m == 2:
                earningsAlloc[i,n,m] = rand.normalvariate(12.0,4.5)
            elif m == 3:
                earningsAlloc[i,n,m] = rand.normalvariate(18.0,7.5)
                if earningsAlloc[i,n,m] > 30:
                    earningsAlloc[i,n,m] = 30
            elif m == 4 or m == 5:
                mu = np.zeros((main.years,1))
                sigma = np.zeros((main.years,1))
                
                muStart = 7.0
                muEnd = 4.0
                
                mu[n] = muStart - ((n / main.years) * (muStart - muEnd))
                sigma[n] = 0.25 * mu[n]
                
                earningsAlloc[i,n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 6:
                mu = np.zeros((main.years,1))
                sigma = np.zeros((main.years,1))
                
                muStart = 7.0
                muEnd = 5.0
                
                mu[n] = muStart - ((n / main.years) * (muStart - muEnd))
                sigma[n] = 0.35 * mu[n]
                
                earningsAlloc[i,n,m] = rand.normalvariate(mu[n],sigma[n])
            elif m == 7:
                earningsAlloc[i,n,m] = 0.05
            elif m == 8:
                earningsAlloc[i,n,m] = 1.5
            elif m == 9:
                earningsAlloc[i,n,m] = 1.0
            elif m == 10:
                earningsAlloc[i,n,m] = 0
            
earningsAlloc = earningsAlloc / 100
meanEarningsAlloc = np.mean(earningsAlloc,axis = 0)

plt.plot(meanEarningsAlloc)