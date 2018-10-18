import main
import taxes as tx
import withholdings as wh
import mortgage as mort

import numpy as np
import matplotlib.pyplot as plt

# savings =     [yr 0, yr 10, yr 20, yr 30, yr 40]

# Investments/Savings
allocations = [[2.5  , 5    , 5    , 10   , 5    ],     #hiDiv
               [2.5  , 7.5  , 7.5  , 12.5 , 5    ],     #ltLowVol
               [2.5  , 7.5  , 7.5  , 12.5 , 5    ],     #largeCap
               [12.5 , 12.5 , 7.5  , 5    , 5    ],     #stHiVol
               [0    , 0    , 0    , 0    , 0    ],     #retRoth401
               [0    , 0    , 0    , 0    , 0    ],     #retTrad401
               [0    , 5    , 12.5 , 0    , 0    ],     #col529
               [5    , 2.5  , 2.5  , 2.5  , 15   ],     #emergFunds
               [35   , 27.5 , 35   , 32.5 , 30   ],     #medTerm
               [17.5 , 22.5 , 12.5 , 15   , 20   ],     #shortTerm
               [22.5 , 10   , 10   , 10   , 15   ]]     #excSpend

#savingsCheck = np.sum(allocations,axis=0)
#print(savingsCheck)

savingsAlloc = np.zeros((main.years,len(allocations)))

for n in range(main.years):
    for m in range(len(allocations)):
        if n == 0:
            savingsAlloc[n,m] = allocations[m][0]
        elif n < int(main.years/4):
            savingsAlloc[n,m] = (((n % int(main.years/4)) / int(main.years/4)) * (allocations[m][1] - allocations[m][0])) + allocations[m][0]
        elif n < int(main.years/4)*2:
            savingsAlloc[n,m] = (((n % int(main.years/4)) / int(main.years/4)) * (allocations[m][2] - allocations[m][1])) + allocations[m][1]
        elif n < int(main.years/4)*3:
            savingsAlloc[n,m] = (((n % int(main.years/4)) / int(main.years/4)) * (allocations[m][3] - allocations[m][2])) + allocations[m][2]
        elif n < main.years-1:
            savingsAlloc[n,m] = (((n % int(main.years/4)) / int(main.years/4)) * (allocations[m][4] - allocations[m][3])) + allocations[m][3]
        else:
            savingsAlloc[n,m] = allocations[m][4]

savingsAlloc = savingsAlloc / 100

netSavings = tx.netIncome - wh.totalWithheld - mort.housePaySum
for n in range(main.years):
    if netSavings[n] < 0:
        netSavings[n] = 0

savingsCont = np.zeros((main.years,len(allocations)))

for n in range(main.years):
    for m in range(len(allocations)):    
        savingsCont[n,m] = savingsAlloc[n,m] * netSavings[n]

#plt.clf()
#plt.plot(netSavings)
#plt.plot(savingsCont[:5]/2)
#print(netSavings[0])
#print(savingsCont[0])
#print(np.sum(savingsCont[0]))