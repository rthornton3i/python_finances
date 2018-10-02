import main
import taxes as tx
import withholdings as wh
import mortgage as mort

import numpy as np
import matplotlib.pyplot as plt

# savings =     [yr 0, yr 10, yr 20, yr 30, yr 40]

# Investments/Savings
allocations = [[7.5  , 7.5  , 12.5 , 15   , 15   ],     #hiDiv
               [7.5  , 7.5  , 7.5  , 15   , 12.5 ],     #ltLowVol
               [7.5  , 10   , 7.5  , 10   , 7.5  ],     #largeCap
               [12.5 , 12.5 , 7.5  , 5    , 0    ],     #stHiVol
               [0    , 0    , 0    , 0    , 0    ],     #retRoth401
               [0    , 0    , 0    , 0    , 0    ],     #retTrad401
               [0    , 5    , 10   , 0    , 0    ],     #col529
               [5    , 2.5  , 5    , 2.5  , 2.5  ],     #emergFunds
               [30   , 25   , 30   , 32.5 , 40   ],     #medTerm
               [15   , 22.5 , 10   , 10   , 10   ],     #shortTerm
               [15   , 7.5  , 10   , 10   , 12.5 ]]     #excSpend

#savingsCheck = np.sum(allocations,axis=0)
#print(savingsCheck)

savingsAlloc = np.zeros((main.years,len(allocations)))

for n in range(main.years):
    for m in range(len(allocations)):
        if n == 0:
            savingsAlloc[n,m] = allocations[m][0]
        elif n < 10:
            savingsAlloc[n,m] = (((n % 10) / 10) * (allocations[m][1] - allocations[m][0])) + allocations[m][0]
        elif n < 20:
            savingsAlloc[n,m] = (((n % 10) / 10) * (allocations[m][2] - allocations[m][1])) + allocations[m][1]
        elif n < 30:
            savingsAlloc[n,m] = (((n % 10) / 10) * (allocations[m][3] - allocations[m][2])) + allocations[m][2]
        elif n < 39:
            savingsAlloc[n,m] = (((n % 10) / 10) * (allocations[m][4] - allocations[m][3])) + allocations[m][3]
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

#print(savingsCont)
#plt.plot(netSavings)