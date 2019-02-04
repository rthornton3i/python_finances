import numpy as np
import math
import matplotlib.pyplot as plt

# Investments/Savings
#                         [yr 0 , yr 10 , yr 20 , yr 30 , yr 40 ]
allocations = np.asarray([[2.5  , 5     , 5     , 10    , 5     ],     #hiDiv
                          [2.5  , 7.5   , 7.5   , 12.5  , 5     ],     #ltLowVol
                          [2.5  , 7.5   , 7.5   , 12.5  , 5     ],     #largeCap
                          [12.5 , 12.5  , 7.5   , 5     , 5     ],     #stHiVol
                          [0    , 0     , 0     , 0     , 0     ],     #retRoth401
                          [0    , 0     , 0     , 0     , 0     ],     #retTrad401
                          [0    , 5     , 12.5  , 0     , 0     ],     #col529
                          [5    , 2.5   , 2.5   , 2.5   , 15    ],     #emergFunds
                          [35   , 27.5  , 35    , 32.5  , 30    ],     #medTerm
                          [17.5 , 22.5  , 12.5  , 15    , 20    ],     #shortTerm
                          [22.5 , 10    , 10    , 10    , 15    ]])    #excSpend

#savingsCheck = np.sum(allocations,axis=0)
#print(savingsCheck)

def savings(years,allocations):
    binWid = years / (np.shape(allocations)[1] - 1)
    accounts = np.shape(allocations)[0]
    savingsAlloc = np.zeros((years,accounts))
    
    for n in range(years):
        for m in range(accounts):
            if n == 0:
                savingsAlloc[n,m] = allocations[m][0]
            elif n > 0 and n < years:
                curBin = math.floor(n / binWid)
                savingsAlloc[n,m] = allocations[m][curBin] + (((n % binWid) / binWid) * (allocations[m][curBin+1] - allocations[m][curBin]))
            else:
                savingsAlloc[n,m] = allocations[m][-1]
    
    savingsAlloc = savingsAlloc / 100
    
#    netSavings = tx.netIncome - wh.totalWithheld - mort.housePaySum
#    for n in range(years):
#        if netSavings[n] < 0:
#            netSavings[n] = 0
#    
#    savingsCont = np.zeros((years,len(allocations)))
#    
#    for n in range(years):
#        for m in range(len(allocations)):    
#            savingsCont[n,m] = savingsAlloc[n,m] * netSavings[n]
            
    return savingsAlloc

savingsAlloc = savings(40,allocations)
print(savingsAlloc)

plt.clf()
plt.plot(savingsAlloc)
#plt.plot(savingsCont[:5]/2)
#print(netSavings[0])
#print(savingsCont[0])
#print(np.sum(savingsCont[0]))