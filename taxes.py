import main
import salary as sal
import mortgage as mort
import deductions as deds

import numpy as np
import matplotlib.pyplot as plt

## Miscellaneous Taxes
socialSecurity = .062
medicare = .0145
medicareAdditional = .009

maxTaxSS = 127200
minTaxAM = 250000

# Social Security
ssTax = np.zeros((main.years,1))

for n in range(main.years):
    if sal.salary[n] < maxTaxSS: 
        ssTax[n] = sal.salary[n] * socialSecurity 
    else:
        ssTax[n] = maxTaxSS * socialSecurity

# Medicare
mTax = np.zeros((main.years,1))

for n in range(main.years):  
    mTax[n] = sal.salary[n] * medicare

# Additional Medicare
amTax = np.zeros((main.years,1))

for n in range(main.years):
    if sal.salary[n] > minTaxAM:
        amTax[n] = sal.salary[n] * medicareAdditional 

miscTaxes = ssTax + mTax + amTax

## State, Local, & Property Taxes
localTaxPercent = 0.025
stateTaxPercent = np.zeros((main.years,1))
stateTaxOwed = np.zeros((main.years,1))
bracketState = np.zeros((main.years,1))
stateGrossIncome = np.zeros((main.years,1))

for n in range(main.years):
    if deds.itemStateDed[n] > deds.stdStateDed[n]:
        stateGrossIncome[n] = sal.salary[n] - deds.totalStateEx[n] - deds.itemStateDed[n]
    else:
        stateGrossIncome[n] = sal.salary[n] - deds.totalStateEx[n] - deds.stdStateDed[n]

bracketState1 = 1000
bracketState2 = 2000
bracketState3 = 3000
bracketState4 = 150000
bracketState5 = 175000
bracketState6 = 225000
bracketState7 = 300000

for n in range(main.years):
    if sal.salary[n] < bracketState1:
        stateTaxPercent[n] = 0.02
        stateTaxOwed[n] = 0
        bracketState[n] = 0
    elif sal.salary[n] < bracketState2:
        stateTaxPercent[n] = 0.03
        stateTaxOwed[n] = 20
        bracketState[n] = bracketState1
    elif sal.salary[n] < bracketState3:
        stateTaxPercent[n] = 0.04
        stateTaxOwed[n] = 50
        bracketState[n] = bracketState2
    elif sal.salary[n] < bracketState4:
        stateTaxPercent[n] = 0.0475
        stateTaxOwed[n] = 90
        bracketState[n] = bracketState3
    elif sal.salary[n] < bracketState5:
        stateTaxPercent[n] = 0.05
        stateTaxOwed[n] = 7072.5
        bracketState[n] = bracketState4
    elif sal.salary[n] < bracketState6:
        stateTaxPercent[n] = 0.0525
        stateTaxOwed[n] = 8322.5
        bracketState[n] = bracketState5
    elif sal.salary[n] < bracketState7:
        stateTaxPercent[n] = 0.055
        stateTaxOwed[n] = 10947.5
        bracketState[n] = bracketState6
    else:
        stateTaxPercent[n] = 0.0575
        stateTaxOwed[n] = 15072.5
        bracketState[n] = bracketState7

stateLocalPropTaxes = np.zeros((main.years,1))

for n in range(main.years):              
    stateLocalPropTaxes[n] = stateTaxOwed[n] + ((stateTaxPercent[n] + localTaxPercent) * (stateGrossIncome[n] - bracketState[n])) + mort.housePropSum[n]

## Federal Taxes
fedTaxPercent = np.zeros((main.years,1))
fedTaxOwed = np.zeros((main.years,1))
bracketFed = np.zeros((main.years,1))
fedGrossIncome = np.zeros((main.years,1))

deds.itemFedDed = deds.itemFedDed + stateLocalPropTaxes

for n in range(main.years):
    if deds.itemFedDed[n] > deds.stdFedDed[n]:
        fedGrossIncome[n] = sal.salary[n] - deds.itemFedDed[n]
    else:
        fedGrossIncome[n] = sal.salary[n] - deds.stdFedDed[n]

bracketFed1 = 19050
bracketFed2 = 77400
bracketFed3 = 165000
bracketFed4 = 315000
bracketFed5 = 400000
bracketFed6 = 600000

for n in range(main.years):
    if sal.salary[n] < bracketFed1:
        fedTaxPercent[n] = 0.1
        fedTaxOwed[n] = 0
        bracketFed[n] = 0
    elif sal.salary[n] < bracketFed2:
        fedTaxPercent[n] = 0.12
        fedTaxOwed[n] = 1905
        bracketFed[n] = bracketFed1
    elif sal.salary[n] < bracketFed3:
        fedTaxPercent[n] = 0.22
        fedTaxOwed[n] = 8907
        bracketFed[n] = bracketFed2
    elif sal.salary[n] < bracketFed4:
        fedTaxPercent[n] = 0.24
        fedTaxOwed[n] = 28179
        bracketFed[n] = bracketFed3
    elif sal.salary[n] < bracketFed5:
        fedTaxPercent[n] = 0.32
        fedTaxOwed[n] = 64179
        bracketFed[n] = bracketFed4
    elif sal.salary[n] < bracketFed6:
        fedTaxPercent[n] = 0.35
        fedTaxOwed[n] = 91379
        bracketFed[n] = bracketFed5
    else:
        fedTaxPercent[n] = 0.37
        fedTaxOwed[n] = 161379
        bracketFed[n] = bracketFed6

fedTaxes = np.zeros((main.years,1))

for n in range(main.years):              
    fedTaxes[n] = fedTaxOwed[n] + (fedTaxPercent[n] * (fedGrossIncome[n] - bracketFed[n]))
    
totalTaxes = fedTaxes + stateLocalPropTaxes

netIncome = sal.salary - totalTaxes

#plt.plot(fedGrossIncome)
#plt.plot(sal.salary)
#plt.plot(netIncome)